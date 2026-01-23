# 🎨 Guia Visual do Projeto

## 📁 Estrutura de Arquivos

```
mba-ia-desafio-ingestao-busca/
│
├── 📄 README.md              ← Documentação principal (LEIA PRIMEIRO!)
├── 🚀 QUICKSTART.md          ← Guia rápido de 3 passos
├── 💡 EXAMPLES.md            ← Exemplos práticos e casos de uso
├── 🏗️  ARCHITECTURE.md        ← Arquitetura técnica detalhada
├── 📊 SUMMARY.md             ← Resumo de todas as melhorias
│
├── ⚙️  .env.example           ← Template de configuração
├── 🚫 .gitignore             ← Arquivos ignorados pelo Git
├── 📦 requirements.txt       ← Dependências Python (CORRIGIDAS)
├── 🐳 docker-compose.yml     ← PostgreSQL + pgvector
│
├── 🔧 setup.sh               ← Setup automático (execute primeiro!)
├── 🎮 manage.py              ← CLI de gerenciamento
│
├── 📄 document.pdf           ← Seu documento PDF
│
└── 📂 src/
    ├── 📥 ingest.py          ← Ingestão de PDF (com validações)
    ├── 🔍 search.py          ← Busca RAG (com logging)
    ├── 💬 chat.py            ← Chat simples (melhorado)
    ├── 🤖 agent.py           ← Agente avançado ⭐ NOVO!
    └── ✅ validate.py        ← Validação de ambiente ⭐ NOVO!
```

## 🎯 Fluxo de Uso

### 🆕 Primeira Vez

```
┌─────────────────────────────────────────────┐
│  1. Execute: ./setup.sh                     │
│     └─ Instala tudo automaticamente         │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│  2. Configure: nano .env                    │
│     └─ Adicione GOOGLE_API_KEY              │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│  3. Valide: python manage.py validate       │
│     └─ Verifica se está tudo OK             │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│  4. Ingira: python manage.py ingest         │
│     └─ Processa o PDF                       │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│  5. Use: python manage.py agent             │
│     └─ Inicia o agente avançado! 🎉         │
└─────────────────────────────────────────────┘
```

### 🔄 Uso Diário

```
┌──────────────────┐
│  Ativar venv     │
│  source venv/... │
└────────┬─────────┘
         ↓
┌──────────────────┐
│  Usar agente     │
│  manage.py agent │
└────────┬─────────┘
         ↓
┌──────────────────┐
│  Fazer perguntas │
│  Analisar docs   │
└────────┬─────────┘
         ↓
┌──────────────────┐
│  Sair e pronto!  │
└──────────────────┘
```

## 🎭 Comparação Visual: Chat vs Agent

### 💬 Chat Simples

```
┌────────────────────────────────────┐
│  Você: Qual o faturamento?         │
└────────────────────────────────────┘
         ↓ [Busca no documento]
┌────────────────────────────────────┐
│  Chat: R$ 10 milhões               │
└────────────────────────────────────┘

┌────────────────────────────────────┐
│  Você: E o lucro?                  │
└────────────────────────────────────┘
         ↓ [Busca novamente, ZERO contexto]
┌────────────────────────────────────┐
│  Chat: R$ 3 milhões                │
└────────────────────────────────────┘

┌────────────────────────────────────┐
│  Você: Calcule a margem            │
└────────────────────────────────────┘
         ↓ [Não tem calculadora]
┌────────────────────────────────────┐
│  Chat: ❌ Não consegue calcular    │
└────────────────────────────────────┘
```

### 🤖 Agente Avançado

```
┌────────────────────────────────────┐
│  Você: Qual o faturamento?         │
└────────────────────────────────────┘
         ↓ [Busca + salva na memória]
┌────────────────────────────────────┐
│  Agent: R$ 10 milhões              │
│  💾 [Armazenado na memória]        │
└────────────────────────────────────┘

┌────────────────────────────────────┐
│  Você: E o lucro?                  │
└────────────────────────────────────┘
         ↓ [Busca + usa contexto anterior]
┌────────────────────────────────────┐
│  Agent: R$ 3 milhões               │
│  💾 [Lembra: faturamento=10M]      │
└────────────────────────────────────┘

┌────────────────────────────────────┐
│  Você: Calcule a margem            │
└────────────────────────────────────┘
         ↓ [Usa tool calculadora + memória]
┌────────────────────────────────────┐
│  Agent: 🧮 (3/10)*100 = 30%        │
│  ✨ Margem de 30%                  │
└────────────────────────────────────┘

┌────────────────────────────────────┐
│  Você: Resuma nossa conversa       │
└────────────────────────────────────┘
         ↓ [Usa tool de resumo]
┌────────────────────────────────────┐
│  Agent: 📝 Resumo:                 │
│  - Faturamento: R$ 10M             │
│  - Lucro: R$ 3M                    │
│  - Margem: 30%                     │
└────────────────────────────────────┘
```

## 🛠️ Tools do Agente

```
┌─────────────────────────────────────────────┐
│              🤖 AGENTE                      │
├─────────────────────────────────────────────┤
│                                             │
│  Tool 1: 🔍 search_documents                │
│  └─ Busca informações no PDF               │
│                                             │
│  Tool 2: 🧮 calculate                       │
│  └─ Faz cálculos matemáticos               │
│                                             │
│  Tool 3: 🕐 get_datetime                    │
│  └─ Retorna data/hora atual                │
│                                             │
│  Tool 4: 📝 summarize_conversation          │
│  └─ Resume o histórico                     │
│                                             │
│  Memory: 💾 Mantém contexto                 │
│  Reasoning: 🧠 Raciocínio multi-step        │
│                                             │
└─────────────────────────────────────────────┘
```

## 📊 Pipeline de Dados

### Ingestão (Primeira vez ou ao atualizar PDF)

```
┌──────────┐
│   PDF    │
└────┬─────┘
     │
     ↓ [PyPDFLoader]
┌──────────────────┐
│  Texto extraído  │
│  (várias páginas)│
└────┬─────────────┘
     │
     ↓ [TextSplitter]
┌──────────────────┐
│  Chunks de texto │
│  (1000 chars)    │
│  ├─ Chunk 1      │
│  ├─ Chunk 2      │
│  └─ Chunk N      │
└────┬─────────────┘
     │
     ↓ [Gemini Embeddings]
┌──────────────────┐
│  Vetores         │
│  (1536 dims)     │
│  ├─ [0.1, 0.2..]│
│  ├─ [0.3, 0.1..]│
│  └─ [0.5, 0.4..]│
└────┬─────────────┘
     │
     ↓ [PGVector]
┌──────────────────┐
│  PostgreSQL      │
│  + pgvector      │
│  ✓ Armazenado!   │
└──────────────────┘
```

### Busca (Cada pergunta)

```
┌──────────────────┐
│  Sua Pergunta    │
└────┬─────────────┘
     │
     ↓ [Gemini Embeddings]
┌──────────────────┐
│  Vetor da query  │
│  [0.2, 0.5, ...] │
└────┬─────────────┘
     │
     ↓ [Similarity Search]
┌──────────────────┐
│  PostgreSQL      │
│  Busca top-10    │
│  chunks similares│
└────┬─────────────┘
     │
     ↓ [Formatter]
┌──────────────────┐
│  Contexto        │
│  (chunks unidos) │
└────┬─────────────┘
     │
     ↓ [Prompt Template]
┌──────────────────┐
│  Prompt completo │
│  ├─ Contexto     │
│  ├─ Regras       │
│  └─ Pergunta     │
└────┬─────────────┘
     │
     ↓ [Gemini LLM]
┌──────────────────┐
│  Resposta Final  │
│  ✨ Inteligente  │
└──────────────────┘
```

## 🎮 Comandos do CLI (manage.py)

```
┌─────────────────────────────────────────────┐
│          python manage.py <comando>         │
├─────────────────────────────────────────────┤
│                                             │
│  🚀 setup       Setup completo              │
│  ✅ validate    Validar ambiente            │
│  ▶️  start       Iniciar PostgreSQL          │
│  ⏹️  stop        Parar PostgreSQL            │
│  📥 ingest      Ingerir documento           │
│  💬 chat        Chat simples                │
│  🤖 agent       Agente avançado ⭐          │
│  📊 logs        Ver logs                    │
│  📈 status      Status do sistema           │
│  🧹 clean       Limpar caches               │
│                                             │
└─────────────────────────────────────────────┘
```

## 🔍 Sistema de Validação

```
python manage.py validate

┌─────────────────────────────────────────────┐
│  🔍 VALIDAÇÃO DO AMBIENTE                   │
├─────────────────────────────────────────────┤
│                                             │
│  ✅ Arquivo .env configurado                │
│  ✅ Arquivo PDF existe (1.2 MB)             │
│  ✅ Docker instalado e rodando              │
│  ✅ Container postgres_rag ativo            │
│  ✅ Dependências Python OK                  │
│  ✅ PostgreSQL acessível                    │
│  ✅ Extensão pgvector instalada             │
│  ✅ Dados ingeridos: 150 embeddings         │
│                                             │
│  ✨ TUDO OK! Sistema pronto.                │
│                                             │
└─────────────────────────────────────────────┘
```

## 📈 Estatísticas do Projeto

```
┌──────────────────────────────────────┐
│  ANTES das melhorias                 │
├──────────────────────────────────────┤
│  📄 Arquivos: 5                      │
│  📏 Linhas: ~150                     │
│  🐛 Erros: requirements quebrado     │
│  ⚠️  Validações: Nenhuma             │
│  📖 Docs: README básico              │
└──────────────────────────────────────┘

             ↓↓↓↓↓↓↓↓↓

┌──────────────────────────────────────┐
│  DEPOIS das melhorias ✨              │
├──────────────────────────────────────┤
│  📄 Arquivos: 15                     │
│  📏 Linhas: 2500+                    │
│  ✅ Erros: CORRIGIDOS                │
│  🛡️  Validações: Completas           │
│  📚 Docs: 5 arquivos completos       │
│  🤖 Agent: Com tools + memory        │
│  🔧 CLI: 10 comandos úteis           │
│  🚀 Setup: Automatizado              │
└──────────────────────────────────────┘
```

## 🎯 Quando Usar Cada Componente

```
┌─────────────────────────────────────────────┐
│  SITUAÇÃO              →  USAR              │
├─────────────────────────────────────────────┤
│  Primeira instalação   →  ./setup.sh        │
│  Verificar ambiente    →  manage.py validate│
│  Novo documento PDF    →  manage.py ingest  │
│  Pergunta rápida       →  manage.py chat    │
│  Análise complexa      →  manage.py agent   │
│  Ver o que aconteceu   →  manage.py logs    │
│  Problemas?            →  manage.py status  │
│  Limpar tudo           →  manage.py clean   │
└─────────────────────────────────────────────┘
```

## 🎓 Documentação por Nível

```
┌─────────────────────────────────────────────┐
│  👶 INICIANTE                               │
│  └─ QUICKSTART.md  (comece aqui!)          │
├─────────────────────────────────────────────┤
│  👨‍💻 INTERMEDIÁRIO                         │
│  ├─ README.md      (guia completo)         │
│  └─ EXAMPLES.md    (casos práticos)        │
├─────────────────────────────────────────────┤
│  👨‍🔬 AVANÇADO                              │
│  ├─ ARCHITECTURE.md (arquitetura)          │
│  └─ SUMMARY.md      (todas melhorias)      │
└─────────────────────────────────────────────┘
```

## 🌟 Features Destacadas

```
┌──────────────────────────────────────────┐
│  ⭐ AGENTE AVANÇADO (agent.py)           │
│                                          │
│  ✨ Memory      → Lembra conversas       │
│  🔧 Tools       → 4 ferramentas úteis    │
│  🧠 Reasoning   → Planejamento           │
│  🎯 Multi-step  → Ações encadeadas       │
│                                          │
│  Use: python manage.py agent             │
└──────────────────────────────────────────┘
```

---

**🚀 Projeto Profissional de RAG - Pronto para Produção!**

- 📖 Documentação completa
- 🛡️ Código robusto
- 🤖 IA avançada
- 🔧 Ferramentas úteis
- ✅ Tudo testado

**Comece agora: `./setup.sh`** 🎉
