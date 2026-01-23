# 🏗️ Arquitetura do Sistema RAG

## Visão Geral

```
┌─────────────────────────────────────────────────────────────┐
│                    USUÁRIO                                   │
│                      ↓ ↑                                     │
├─────────────────────────────────────────────────────────────┤
│              INTERFACE (chat.py / agent.py)                  │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Memory     │  │     LLM      │  │    Tools     │     │
│  │  (histórico) │  │  (Gemini)    │  │ (customiz.)  │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│                           │                                  │
│                           ↓                                  │
│                  ┌─────────────────┐                        │
│                  │   RAG Pipeline   │                        │
│                  └─────────────────┘                        │
│                           │                                  │
├───────────────────────────┼──────────────────────────────────┤
│                           ↓                                  │
│              ┌──────────────────────────┐                   │
│              │   Vector Store (PGVector) │                   │
│              │   PostgreSQL + pgvector   │                   │
│              └──────────────────────────┘                   │
└─────────────────────────────────────────────────────────────┘
```

## Componentes Principais

### 1. Camada de Interface

#### chat.py - Chat Simples
```python
Usuário → Input
    ↓
search.py (RAG simples)
    ↓
Resposta
```

**Características:**
- Interface básica de pergunta/resposta
- Sem memória entre perguntas
- RAG direto: pergunta → busca → resposta
- Ideal para: consultas rápidas e independentes

#### agent.py - Agente Avançado
```python
Usuário → Input
    ↓
Agent Executor
    ├→ Memory (histórico)
    ├→ Tools (search, calc, etc)
    ├→ LLM (reasoning)
    └→ Multi-step execution
    ↓
Resposta enriquecida
```

**Características:**
- Mantém contexto conversacional
- Acesso a múltiplas tools
- Capacidade de reasoning multi-step
- Ideal para: análises complexas e conversas longas

### 2. Camada de Processamento

#### ingest.py - Pipeline de Ingestão

```
PDF File
    ↓
PyPDFLoader (leitura)
    ↓
RecursiveCharacterTextSplitter (chunking)
    ├─ chunk_size: 1000 caracteres
    └─ chunk_overlap: 150 caracteres
    ↓
GoogleGenerativeAIEmbeddings (vetorização)
    └─ modelo: embedding-001
    ↓
PGVector (armazenamento)
    └─ PostgreSQL + pgvector extension
```

**Fluxo detalhado:**
1. **Leitura**: Extrai texto do PDF
2. **Chunking**: Divide em pedaços sobrepostos
3. **Embedding**: Converte texto em vetores (1536 dimensões)
4. **Armazenamento**: Salva no banco com índice HNSW

#### search.py - Pipeline de Busca

```
Query (pergunta do usuário)
    ↓
Embedding da query
    ↓
Similarity Search (PGVector)
    ├─ Busca por similaridade de cosseno
    └─ Retorna top-k chunks (default: 10)
    ↓
Contexto montado
    ↓
Prompt Template
    ├─ Contexto: chunks relevantes
    ├─ Regras: responder apenas com base no contexto
    └─ Pergunta: query original
    ↓
LLM (Gemini 1.5 Flash)
    └─ Gera resposta baseada no contexto
    ↓
Resposta final
```

### 3. Camada de Dados

#### PostgreSQL + pgVector

```sql
-- Estrutura simplificada

langchain_pg_collection
├─ uuid (PK)
├─ name (ex: "document_vectors")
└─ cmetadata

langchain_pg_embedding
├─ id (PK)
├─ collection_id (FK)
├─ embedding (vector[1536])  ← Vetor do embedding
├─ document (text)            ← Conteúdo do chunk
├─ cmetadata (jsonb)          ← Metadados (página, etc)
└─ custom_id

-- Índice para busca rápida
CREATE INDEX ON langchain_pg_embedding 
USING hnsw (embedding vector_cosine_ops);
```

**Características:**
- **HNSW Index**: Busca aproximada rápida (ANN)
- **Cosine Similarity**: Métrica de similaridade
- **Escalável**: Milhões de vetores
- **ACID**: Transações garantidas

### 4. Camada de IA

#### Google Gemini

```
┌─────────────────────────────────────┐
│  GoogleGenerativeAIEmbeddings       │
│  modelo: embedding-001              │
│  dimensões: 1536                    │
│  uso: vetorização de texto          │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│  ChatGoogleGenerativeAI             │
│  modelo: gemini-1.5-flash           │
│  temperatura: 0.0-0.3               │
│  uso: geração de respostas          │
└─────────────────────────────────────┘
```

## Fluxo de Dados Completo

### Ingestão (uma vez ou quando atualizar documento)

```
1. Usuário executa: python src/ingest.py

2. Sistema:
   ├─ Valida .env, PDF e conexão
   ├─ Carrega PDF (PyPDFLoader)
   ├─ Divide em chunks (TextSplitter)
   │   └─ 1000 chars, overlap 150
   ├─ Para cada chunk:
   │   ├─ Chama API Gemini (embedding)
   │   ├─ Recebe vetor [1536 floats]
   │   └─ Armazena no PostgreSQL
   └─ Log: "N chunks ingeridos"

3. Resultado: Banco populado com vetores
```

### Busca (cada pergunta)

```
1. Usuário faz pergunta

2. Sistema:
   ├─ Gera embedding da pergunta
   │   └─ API Gemini → vetor [1536]
   │
   ├─ Busca similaridade no banco
   │   ├─ SELECT ... ORDER BY embedding <=> query_vector
   │   ├─ Usa índice HNSW (rápido)
   │   └─ Retorna top-10 chunks
   │
   ├─ Monta contexto
   │   └─ Concatena chunks relevantes
   │
   ├─ Monta prompt
   │   ├─ Sistema: regras
   │   ├─ Contexto: chunks
   │   └─ Pergunta: query
   │
   ├─ Envia para LLM
   │   └─ API Gemini (generação)
   │
   └─ Retorna resposta
```

### Agente (com tools e memory)

```
1. Usuário faz pergunta

2. Agent Executor:
   ├─ Carrega histórico (memory)
   │
   ├─ Analisa pergunta
   │   ├─ Precisa buscar no documento?
   │   ├─ Precisa calcular algo?
   │   ├─ Precisa data/hora?
   │   └─ Precisa resumir conversa?
   │
   ├─ Planeja execução (reasoning)
   │   └─ Determina sequence de tools
   │
   ├─ Executa tools (até 5 iterações)
   │   ├─ Tool 1: search_documents
   │   │   └─ Busca RAG normal
   │   ├─ Tool 2: calculate
   │   │   └─ eval(expressão)
   │   ├─ Tool 3: get_datetime
   │   │   └─ datetime.now()
   │   └─ Tool 4: summarize_conversation
   │       └─ Resume histórico
   │
   ├─ Combina resultados
   │   └─ LLM sintetiza resposta final
   │
   ├─ Salva no histórico (memory)
   │
   └─ Retorna resposta enriquecida
```

## Tecnologias e Bibliotecas

### Python Core
```python
python 3.10+           # Runtime
dotenv                 # Variáveis de ambiente
logging                # Logs estruturados
pathlib                # Manipulação de paths
```

### LangChain Stack
```python
langchain              # Framework core
langchain-core         # Abstrações base
langchain-community    # Integrações (PDF, etc)
langchain-google-genai # Integração Google
langchain-postgres     # Integração PostgreSQL
langchain-text-splitters # Chunking
```

### Database & Vectors
```python
psycopg2-binary        # Driver PostgreSQL
pgvector               # Client pgvector
SQLAlchemy             # ORM
```

### AI & ML
```python
google-generativeai    # API Google Gemini
tiktoken               # Tokenização
numpy                  # Operações numéricas
```

### Utilities
```python
pypdf                  # Leitura de PDF
pydantic               # Validação de dados
requests               # HTTP client
```

## Padrões de Projeto Utilizados

### 1. Pipeline Pattern
```python
# Ingestão
PDF → Loader → Splitter → Embedder → Store

# Busca
Query → Embedder → Retriever → Formatter → LLM
```

### 2. Strategy Pattern
```python
# Diferentes estratégias de busca
- Similarity Search
- MMR (Maximum Marginal Relevance)
- Threshold-based
```

### 3. Chain of Responsibility
```python
# Agent executor
Input → Agent → Tools → LLM → Output
```

### 4. Repository Pattern
```python
# PGVector como repositório
- from_documents()
- similarity_search()
- as_retriever()
```

### 5. Builder Pattern
```python
# Construção de chains
chain = (
    {"context": retriever | formatter, "question": passthrough}
    | prompt
    | llm
)
```

## Configurações e Otimizações

### Chunking
```python
chunk_size = 1000      # Tamanho ideal para contexto
chunk_overlap = 150    # Preserva contexto entre chunks
```

### Embedding
```python
model = "embedding-001"  # Google, 1536 dims
batch_size = 100         # Processa em lotes
```

### Retrieval
```python
k = 10                   # Top-k resultados
search_type = "similarity"  # Tipo de busca
```

### LLM
```python
model = "gemini-1.5-flash"  # Rápido e eficiente
temperature = 0.0           # Determinístico (busca)
temperature = 0.3           # Criativo (agent)
max_tokens = 2048           # Limite de resposta
```

### Database
```python
# pgvector index
index_type = "hnsw"         # Hierarquical NSW
m = 16                      # Conexões por nó
ef_construction = 64        # Qualidade do índice
```

## Segurança

### API Keys
```python
# Nunca commitar .env
# Usar variáveis de ambiente
# Validar antes de usar
```

### Input Sanitization
```python
# Validar queries
# Limitar tamanho de input
# Escapar caracteres especiais (calc)
```

### Database
```python
# Usar prepared statements
# Limitar queries
# Timeout em conexões
```

## Monitoramento

### Logs
```python
ingest.log     # Pipeline de ingestão
agent.log      # Execução do agente
```

### Métricas
```python
- Tempo de ingestão
- Tempo de busca
- Número de chunks
- Taxa de sucesso
- Uso de API
```

## Escalabilidade

### Vertical (mais recursos)
```
- PostgreSQL com mais RAM
- Índices otimizados
- Cache de embeddings
```

### Horizontal (mais instâncias)
```
- PostgreSQL replicado
- Load balancer
- Cache distribuído (Redis)
- Queue de ingestão (Celery)
```

## Extensibilidade

### Novos Documentos
```python
# Adicionar loaders
from langchain_community.document_loaders import (
    UnstructuredWordDocumentLoader,
    UnstructuredExcelLoader,
    TextLoader,
)
```

### Novos Tools
```python
# Adicionar ao agent
def custom_tool(input: str) -> str:
    # Sua lógica
    return result

tools.append(Tool(
    name="custom",
    func=custom_tool,
    description="..."
))
```

### Novos LLMs
```python
# Trocar provider
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

llm = ChatOpenAI(model="gpt-4")
```

---

**Arquitetura criada para:**
- ✅ Performance
- ✅ Escalabilidade
- ✅ Manutenibilidade
- ✅ Extensibilidade
- ✅ Confiabilidade
