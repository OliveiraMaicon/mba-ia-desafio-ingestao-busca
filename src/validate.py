"""
Utilitário de validação e diagnóstico do ambiente
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def check_env_file():
    """Verifica se o arquivo .env existe e está configurado."""
    print("\n📋 Verificando arquivo .env...")
    
    env_path = Path(".env")
    if not env_path.exists():
        print("  ❌ Arquivo .env não encontrado")
        print("  💡 Crie um arquivo .env baseado em .env.example:")
        print("     cp .env.example .env")
        return False
    
    print("  ✓ Arquivo .env encontrado")
    
    # Carregar variáveis
    load_dotenv()
    
    # Verificar variáveis obrigatórias
    required_vars = {
        "GOOGLE_API_KEY": "Chave de API do Google",
        "PDF_PATH": "Caminho do arquivo PDF",
        "CONNECTION_STRING": "String de conexão do PostgreSQL"
    }
    
    all_ok = True
    for var, description in required_vars.items():
        value = os.getenv(var)
        if not value or value.startswith("sua_chave") or value == "":
            print(f"  ❌ {var} não configurada ({description})")
            all_ok = False
        else:
            masked_value = value[:10] + "..." if len(value) > 10 else value
            print(f"  ✓ {var}: {masked_value}")
    
    return all_ok


def check_pdf_file():
    """Verifica se o arquivo PDF existe."""
    print("\n📄 Verificando arquivo PDF...")
    
    load_dotenv()
    pdf_path = Path(os.getenv("PDF_PATH", "document.pdf"))
    
    if not pdf_path.exists():
        print(f"  ❌ Arquivo PDF não encontrado: {pdf_path}")
        print(f"  💡 Certifique-se de que o arquivo existe ou ajuste PDF_PATH no .env")
        return False
    
    if not pdf_path.suffix.lower() == '.pdf':
        print(f"  ❌ Arquivo não é um PDF: {pdf_path}")
        return False
    
    size_kb = pdf_path.stat().st_size / 1024
    print(f"  ✓ PDF encontrado: {pdf_path} ({size_kb:.2f} KB)")
    return True


def check_database():
    """Verifica conexão com o banco de dados."""
    print("\n🗄️  Verificando banco de dados PostgreSQL...")
    
    load_dotenv()
    connection_string = os.getenv("CONNECTION_STRING")
    
    try:
        engine = create_engine(connection_string)
        with engine.connect() as conn:
            # Testar conexão
            conn.execute(text("SELECT 1"))
            print("  ✓ Conexão com PostgreSQL OK")
            
            # Verificar extensão pgvector
            result = conn.execute(text(
                "SELECT EXISTS(SELECT 1 FROM pg_extension WHERE extname = 'vector')"
            ))
            has_vector = result.scalar()
            
            if has_vector:
                print("  ✓ Extensão pgvector instalada")
            else:
                print("  ❌ Extensão pgvector NÃO instalada")
                print("  💡 Execute: docker compose up -d")
                return False
            
            # Verificar se há dados ingeridos
            collection_name = os.getenv("COLLECTION_NAME", "document_vectors")
            result = conn.execute(text(
                f"SELECT COUNT(*) FROM langchain_pg_embedding WHERE collection_id = "
                f"(SELECT uuid FROM langchain_pg_collection WHERE name = '{collection_name}')"
            ))
            count = result.scalar() or 0
            
            if count > 0:
                print(f"  ✓ Dados encontrados: {count} embeddings na collection '{collection_name}'")
            else:
                print(f"  ⚠️  Nenhum dado ingerido ainda")
                print(f"  💡 Execute: python src/ingest.py")
            
        return True
        
    except Exception as e:
        print(f"  ❌ Erro ao conectar: {e}")
        print("  💡 Certifique-se de que o PostgreSQL está rodando:")
        print("     docker compose up -d")
        return False


def check_dependencies():
    """Verifica se as dependências Python estão instaladas."""
    print("\n📦 Verificando dependências Python...")
    
    required_packages = [
        ("langchain", "LangChain"),
        ("langchain_google_genai", "LangChain Google GenAI"),
        ("langchain_postgres", "LangChain Postgres"),
        ("psycopg", "psycopg (driver PostgreSQL)"),
        ("pgvector", "pgvector"),
        ("dotenv", "python-dotenv"),
    ]
    
    all_ok = True
    for package, name in required_packages:
        try:
            __import__(package)
            print(f"  ✓ {name}")
        except ImportError:
            print(f"  ❌ {name} não instalado")
            all_ok = False
    
    if not all_ok:
        print("\n  💡 Instale as dependências:")
        print("     pip install -r requirements.txt")
    
    return all_ok


def check_docker():
    """Verifica se o Docker está instalado e o container está rodando."""
    print("\n🐳 Verificando Docker...")
    
    import subprocess
    
    # Verificar se docker está instalado
    try:
        result = subprocess.run(
            ["docker", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print(f"  ✓ Docker instalado: {result.stdout.strip()}")
        else:
            print("  ❌ Docker não encontrado")
            return False
    except Exception as e:
        print(f"  ❌ Erro ao verificar Docker: {e}")
        return False
    
    # Verificar se container está rodando
    try:
        result = subprocess.run(
            ["docker", "ps", "--filter", "name=postgres_rag", "--format", "{{.Status}}"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.stdout.strip():
            print(f"  ✓ Container postgres_rag: {result.stdout.strip()}")
            return True
        else:
            print("  ⚠️  Container postgres_rag não está rodando")
            print("  💡 Inicie o container: docker compose up -d")
            return False
    except Exception as e:
        print(f"  ⚠️  Não foi possível verificar containers: {e}")
        return False


def main():
    """Executa todas as validações."""
    print("=" * 70)
    print("  🔍 DIAGNÓSTICO DO AMBIENTE - Sistema RAG")
    print("=" * 70)
    
    checks = [
        ("Arquivo .env", check_env_file),
        ("Arquivo PDF", check_pdf_file),
        ("Docker", check_docker),
        ("Dependências Python", check_dependencies),
        ("Banco de Dados", check_database),
    ]
    
    results = {}
    for name, check_func in checks:
        try:
            results[name] = check_func()
        except Exception as e:
            logger.error(f"Erro ao verificar {name}: {e}")
            results[name] = False
    
    # Resumo
    print("\n" + "=" * 70)
    print("  📊 RESUMO")
    print("=" * 70)
    
    for name, status in results.items():
        icon = "✅" if status else "❌"
        print(f"  {icon} {name}")
    
    all_ok = all(results.values())
    
    if all_ok:
        print("\n✅ Tudo OK! O sistema está pronto para uso.")
        print("\nPróximos passos:")
        print("  1. Se ainda não ingeriu dados: python src/ingest.py")
        print("  2. Para chat simples: python src/chat.py")
        print("  3. Para agente avançado: python src/agent.py")
    else:
        print("\n⚠️  Alguns problemas foram encontrados. Resolva-os antes de continuar.")
        print("\nGuia rápido de resolução:")
        if not results.get("Arquivo .env"):
            print("  1. Copie .env.example para .env e configure as variáveis")
        if not results.get("Docker"):
            print("  2. Instale o Docker e inicie o container: docker compose up -d")
        if not results.get("Dependências Python"):
            print("  3. Instale as dependências: pip install -r requirements.txt")
    
    print()
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
