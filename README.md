# Desafio MBA Engenharia de Software com IA - Full Cycle

## Ingestão e Busca Semântica com LangChain e Postgres

Este projeto implementa um sistema de ingestão e busca semântica de documentos PDF utilizando LangChain, PostgreSQL com pgVector e modelos de linguagem da Google.

### Pré-requisitos

- Python 3.x
- Docker e Docker Compose
- Uma chave de API da Google para o Gemini

### Configuração

1. **Crie o arquivo de ambiente:**

   Crie um arquivo chamado `.env` na raiz do projeto e adicione sua chave de API da Google:

   ```
   GOOGLE_API_KEY=SUA_CHAVE_DE_API_AQUI
   PDF_PATH=document.pdf
   CONNECTION_STRING="postgresql+psycopg2://postgres:postgres@localhost:5432/rag"
   ```

2. **Instale as dependências:**

   É recomendado criar um ambiente virtual antes de instalar as dependências.

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

### Execução

1. **Inicie o banco de dados:**

   Execute o comando abaixo para iniciar o contêiner do PostgreSQL com a extensão pgVector.

   ```bash
   docker compose up -d
   ```

2. **Execute a ingestão do PDF:**

   Este comando irá processar o PDF, gerar os embeddings e armazená-los no banco de dados.

   ```bash
   python src/ingest.py
   ```

3. **Inicie o chat:**

   Agora você pode interagir com o sistema. Execute o comando abaixo para iniciar o chat no terminal.

   ```bash
   python src/chat.py
   ```

   Faça suas perguntas sobre o conteúdo do documento PDF e o sistema irá respondê-las.