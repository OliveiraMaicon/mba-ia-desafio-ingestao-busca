# Desafio MBA Engenharia de Software com IA - Full Cycle

## Sistema Avançado de RAG (Retrieval Augmented Generation)

Este projeto implementa um sistema completo de ingestão e busca semântica utilizando:
- **LangChain** para orquestração de LLMs
- **PostgreSQL + pgVector** para armazenamento de embeddings
- **Google Gemini** para embeddings e geração de texto
- **Agente de IA** com memory, tools e reasoning

### 🎯 Funcionalidades

#### Sistema Básico (chat.py)
- ✅ Busca semântica em documentos PDF
- ✅ RAG (Retrieval Augmented Generation)
- ✅ Interface de chat interativa
- ✅ Respostas baseadas apenas no documento

#### Sistema Avançado (agent.py)
- 🤖 **Agente de IA com capacidades expandidas**
- 💾 **Memory**: Mantém contexto da conversação
- 🛠️ **Tools customizadas**:
  - Busca semântica no documento
  - Data/hora atual
  - Calculadora matemática
  - Resumo de conversação
- 🧠 **Multi-step reasoning**
- 📊 **Histórico persistente de conversas**

### 📋 Pré-requisitos

- Python 3.10+
- Docker e Docker Compose
- Chave de API do Google (Gemini)

### 🚀 Setup Rápido

#### Opção 1: Setup Automático (Recomendado)

```bash
# Executar script de setup
./setup.sh

# Siga as instruções na tela
```

#### Opção 2: Setup Manual

1. **Crie o arquivo de ambiente:**

   ```bash
   cp .env.example .env
   ```

   Edite o arquivo `.env` e adicione sua chave de API:

   ```
   GOOGLE_API_KEY=sua_chave_de_api_aqui
   PDF_PATH=document.pdf
   CONNECTION_STRING="postgresql+psycopg2://postgres:postgres@localhost:5432/rag"
   ```

2. **Crie o ambiente virtual e instale as dependências:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Inicie o banco de dados:**

   ```bash
   docker compose up -d
   ```

4. **Verifique a configuração:**

   ```bash
   python src/validate.py
   ```

### 📚 Uso

#### 1. Ingerir o documento PDF

```bash
python src/ingest.py
```

Este comando:
- Carrega o PDF especificado em `PDF_PATH`
- Divide em chunks de texto
- Gera embeddings usando Google Gemini
- Armazena no PostgreSQL com pgVector

**Logs:** Veja `ingest.log` para detalhes

#### 2. Chat Simples (RAG Básico)

```bash
python src/chat.py
```

Interface de chat simples com:
- Busca semântica
- Respostas baseadas no documento
- Comandos: `sair`, `ajuda`, `limpar`

#### 3. Agente Avançado (Recomendado)

```bash
python src/agent.py
```

Agente de IA avançado com:
- **Memory**: Mantém contexto entre perguntas
- **Tools**: Acesso a ferramentas customizadas
- **Reasoning**: Capacidade de raciocínio multi-step

**Exemplos de uso:**

```
Você: Qual o faturamento da empresa?
Agente: [Busca no documento e responde]

Você: E em relação ao ano anterior, aumentou?
Agente: [Usa contexto da pergunta anterior para responder]

Você: Calcule 15% desse valor
Agente: [Usa tool de calculadora]

Você: Que horas são?
Agente: [Usa tool de data/hora]

Você: Resuma nossa conversa
Agente: [Usa tool de resumo]
```

**Logs:** Veja `agent.log` para detalhes

### 🔍 Diagnóstico e Validação

```bash
python src/validate.py
```

Verifica:
- ✅ Arquivo `.env` configurado
- ✅ Arquivo PDF existe
- ✅ Docker está rodando
- ✅ Dependências instaladas
- ✅ PostgreSQL acessível
- ✅ Extensão pgVector instalada
- ✅ Dados ingeridos

### 📁 Estrutura do Projeto

```
├── docker-compose.yml      # Configuração do PostgreSQL
├── requirements.txt        # Dependências Python (CORRIGIDAS)
├── .env.example           # Template de configuração
├── setup.sh               # Script de setup automático
├── README.md              # Esta documentação
└── src/
    ├── ingest.py          # Ingestão de PDF com validações
    ├── search.py          # Busca RAG com logging
    ├── chat.py            # Interface de chat melhorada
    ├── agent.py           # 🆕 Agente avançado com tools
    └── validate.py        # 🆕 Validação de ambiente
```

### 🛠️ Arquitetura do Agente

```
┌─────────────────────────────────────────────────────────┐
│                    Agente de IA                         │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   Memory    │  │     LLM      │  │    Tools     │  │
│  │ (histórico) │  │ (Gemini 2.0) │  │ (customiz.)  │  │
│  └─────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
            ┌─────────────────────────────┐
            │      Vector Store (RAG)      │
            │   PostgreSQL + pgVector      │
            └─────────────────────────────┘
```

### 🔧 Configurações Avançadas

Todas as configurações podem ser ajustadas no arquivo `.env`:

```bash
# Modelos
EMBEDDING_MODEL=models/embedding-001
LLM_MODEL=gemini-2.0-flash-lite
TEMPERATURE=0.3                    # Criatividade (0-1)

# Busca
SEARCH_K=10                        # Número de chunks retornados

# Chunking
CHUNK_SIZE=1000                    # Tamanho dos chunks
CHUNK_OVERLAP=150                  # Sobreposição entre chunks

# Database
COLLECTION_NAME=document_vectors   # Nome da collection
```

### 🐛 Troubleshooting

#### Erro de instalação do requirements.txt
```bash
# As versões foram corrigidas para compatibilidade
pip install --upgrade pip
pip install -r requirements.txt
```

#### PostgreSQL não conecta
```bash
# Verificar se está rodando
docker ps | grep postgres_rag

# Reiniciar
docker compose down
docker compose up -d

# Ver logs
docker logs postgres_rag
```

#### Erro "Nenhum dado encontrado"
```bash
# Verificar ingestão
python src/validate.py

# Re-ingerir dados
python src/ingest.py
```

#### Erro de API Key
```bash
# Verificar se está configurada
cat .env | grep GOOGLE_API_KEY

# Testar API
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('GOOGLE_API_KEY'))"
```

### 📊 Logs e Monitoramento

- `ingest.log` - Log de ingestão de documentos
- `agent.log` - Log do agente avançado
- Terminal - Logs em tempo real

### 📝 Comandos Úteis

```bash
# Ativar ambiente
source venv/bin/activate

# Validar ambiente
python src/validate.py

# Ingerir documento
python src/ingest.py

# Chat simples
python src/chat.py

# Agente avançado
python src/agent.py

# Ver logs
tail -f ingest.log
tail -f agent.log

# Parar PostgreSQL
docker compose down

# Ver dados no banco
docker exec -it postgres_rag psql -U postgres -d rag -c "SELECT COUNT(*) FROM langchain_pg_embedding;"
```