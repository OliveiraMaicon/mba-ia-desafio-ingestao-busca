#!/bin/bash

echo "======================================================================"
echo "  🚀 SETUP AUTOMÁTICO - Sistema RAG com LangChain"
echo "======================================================================"
echo ""

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Função para print colorido
print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_info() {
    echo -e "${YELLOW}ℹ${NC} $1"
}

# 1. Verificar Python
echo "1️⃣  Verificando Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    print_success "Python encontrado: $PYTHON_VERSION"
else
    print_error "Python 3 não encontrado. Instale Python 3.x"
    exit 1
fi
echo ""

# 2. Verificar Docker
echo "2️⃣  Verificando Docker..."
if command -v docker &> /dev/null; then
    DOCKER_VERSION=$(docker --version)
    print_success "Docker encontrado: $DOCKER_VERSION"
else
    print_error "Docker não encontrado. Instale Docker Desktop"
    exit 1
fi
echo ""

# 3. Criar ambiente virtual (se não existir)
echo "3️⃣  Configurando ambiente virtual Python..."
if [ ! -d "venv" ]; then
    print_info "Criando ambiente virtual..."
    python3 -m venv venv
    print_success "Ambiente virtual criado"
else
    print_info "Ambiente virtual já existe"
fi
echo ""

# 4. Ativar ambiente virtual e instalar dependências
echo "4️⃣  Instalando dependências Python..."
source venv/bin/activate
pip install --upgrade pip > /dev/null 2>&1
print_info "Instalando pacotes do requirements.txt..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    print_success "Dependências instaladas com sucesso"
else
    print_error "Erro ao instalar dependências"
    exit 1
fi
echo ""

# 5. Configurar arquivo .env
echo "5️⃣  Configurando arquivo .env..."
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        print_success "Arquivo .env criado a partir do .env.example"
        print_info "⚠️  IMPORTANTE: Edite o arquivo .env e configure:"
        echo "     - GOOGLE_API_KEY (obrigatório)"
        echo "     - PDF_PATH (se necessário)"
    else
        print_error "Arquivo .env.example não encontrado"
        exit 1
    fi
else
    print_info "Arquivo .env já existe"
fi
echo ""

# 6. Iniciar PostgreSQL com Docker
echo "6️⃣  Iniciando PostgreSQL com pgvector..."
print_info "Executando: docker compose up -d"
docker compose up -d

if [ $? -eq 0 ]; then
    print_success "PostgreSQL iniciado com sucesso"
    print_info "Aguardando PostgreSQL ficar pronto..."
    sleep 5
else
    print_error "Erro ao iniciar PostgreSQL"
    exit 1
fi
echo ""

# 7. Verificar ambiente
echo "7️⃣  Verificando configuração do ambiente..."
python3 src/validate.py
echo ""

# Instruções finais
echo "======================================================================"
echo "  ✅ SETUP CONCLUÍDO!"
echo "======================================================================"
echo ""
echo "📝 Próximos passos:"
echo ""
echo "1. Configure suas credenciais:"
echo "   Edite o arquivo .env e adicione sua GOOGLE_API_KEY"
echo ""
echo "2. Ative o ambiente virtual:"
echo "   source venv/bin/activate"
echo ""
echo "3. Ingira o documento PDF:"
echo "   python src/ingest.py"
echo ""
echo "4. Escolha uma interface:"
echo "   python src/chat.py      # Chat simples"
echo "   python src/agent.py     # Agente avançado com tools"
echo ""
echo "🔍 Para diagnóstico completo:"
echo "   python src/validate.py"
echo ""
