# 🚀 Guia Rápido de Início

## Setup em 3 passos

### 1. Setup Automático
```bash
./setup.sh
```

### 2. Configure suas credenciais
```bash
# Edite o arquivo .env
nano .env

# Adicione sua chave:
GOOGLE_API_KEY=sua_chave_aqui
```

### 3. Use o sistema
```bash
# Ative o ambiente
source venv/bin/activate

# Ingira o documento
python src/ingest.py

# Use o agente avançado (recomendado)
python src/agent.py

# OU use o chat simples
python src/chat.py
```

## 🛠️ Gerenciamento Simplificado

Use o script `manage.py` para comandos rápidos:

```bash
# Ver ajuda
python manage.py

# Validar ambiente
python manage.py validate

# Iniciar/parar banco
python manage.py start
python manage.py stop

# Ingerir dados
python manage.py ingest

# Iniciar chat
python manage.py chat

# Iniciar agente
python manage.py agent

# Ver logs
python manage.py logs

# Ver status
python manage.py status

# Limpar caches
python manage.py clean
```

## 🐛 Problemas Comuns

### Erro ao instalar requirements.txt
```bash
# Use Python 3.10+
python3 --version

# Atualize pip
pip install --upgrade pip

# Reinstale
pip install -r requirements.txt
```

### PostgreSQL não inicia
```bash
# Verifique Docker
docker ps

# Restart limpo
docker compose down
docker compose up -d

# Aguarde alguns segundos
sleep 5
```

### Erro "GOOGLE_API_KEY não encontrada"
```bash
# Verifique se o .env existe
ls -la .env

# Verifique o conteúdo
cat .env | grep GOOGLE_API_KEY

# Se não existir, copie do exemplo
cp .env.example .env

# Edite e adicione sua chave
nano .env
```

### Erro "Nenhum dado encontrado"
```bash
# Valide primeiro
python src/validate.py

# Se necessário, re-ingira
python src/ingest.py
```

## 📊 Diferenças entre Chat e Agent

### Chat Simples (src/chat.py)
- Interface básica de perguntas e respostas
- Busca RAG simples
- Sem memória entre perguntas
- Mais rápido
- **Use para**: Consultas rápidas e independentes

### Agente Avançado (src/agent.py) ⭐ RECOMENDADO
- Interface inteligente com IA
- Memory: mantém contexto
- Tools: calculadora, data/hora, resumos
- Multi-step reasoning
- **Use para**: Conversas complexas e análises

## 💡 Exemplos de Uso

### Chat Simples
```
Você: Qual o faturamento da empresa?
Chat: [responde com dados do documento]

Você: E o lucro?
Chat: [busca novamente, sem contexto anterior]
```

### Agente Avançado
```
Você: Qual o faturamento da empresa?
Agente: [busca e responde]

Você: E o lucro, em porcentagem?
Agente: [usa contexto anterior + calcula]

Você: Isso é bom?
Agente: [compara com dados do documento]

Você: Resuma nossa conversa
Agente: [resume tudo que foi discutido]
```

## 📁 Arquivos Importantes

```
.env            # Suas configurações (CRIE ESTE!)
.env.example    # Template
requirements.txt # Dependências (CORRIGIDAS)
setup.sh        # Setup automático
manage.py       # Gerenciador de comandos

src/
├── ingest.py   # Ingestão de PDF
├── chat.py     # Chat simples
├── agent.py    # Agente avançado ⭐
└── validate.py # Validação
```

## 🔍 Validação Completa

Sempre que tiver dúvidas, execute:

```bash
python src/validate.py
```

Isso verifica:
- ✅ Arquivo .env configurado
- ✅ PDF existe
- ✅ Docker rodando
- ✅ Dependências instaladas
- ✅ PostgreSQL acessível
- ✅ Dados ingeridos

## 📞 Suporte

Se algo não funcionar:

1. Execute `python src/validate.py`
2. Leia as mensagens de erro
3. Siga as sugestões mostradas
4. Verifique os logs: `python manage.py logs`

## 🎯 Fluxo Recomendado

```bash
# 1. Setup (uma vez)
./setup.sh

# 2. Configure .env (uma vez)
nano .env

# 3. Valide
python manage.py validate

# 4. Ingira dados (quando mudar o PDF)
python manage.py ingest

# 5. Use o agente (quantas vezes quiser)
python manage.py agent
```

---

**Pronto!** Seu sistema RAG está configurado. Use `python manage.py agent` para começar! 🚀
