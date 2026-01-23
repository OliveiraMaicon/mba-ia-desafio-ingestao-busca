#!/usr/bin/env python3
"""
Script de gerenciamento do sistema RAG
Fornece comandos úteis para operação do sistema
"""

import sys
import subprocess
import argparse
from pathlib import Path


def run_command(cmd, description):
    """Executa um comando e exibe o resultado."""
    print(f"\n{'='*60}")
    print(f"  {description}")
    print(f"{'='*60}\n")
    
    try:
        result = subprocess.run(cmd, shell=True, check=True)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Erro ao executar: {e}")
        return False


def setup():
    """Executa o setup completo do sistema."""
    return run_command("./setup.sh", "🚀 Setup Completo do Sistema")


def validate():
    """Valida a configuração do ambiente."""
    return run_command(f"{sys.executable} src/validate.py", "🔍 Validando Ambiente")


def start_db():
    """Inicia o PostgreSQL."""
    return run_command("docker compose up -d", "🗄️  Iniciando PostgreSQL")


def stop_db():
    """Para o PostgreSQL."""
    return run_command("docker compose down", "🛑 Parando PostgreSQL")


def ingest():
    """Executa a ingestão do documento."""
    return run_command(f"{sys.executable} src/ingest.py", "📄 Ingerindo Documento")


def chat():
    """Inicia o chat simples."""
    return run_command(f"{sys.executable} src/chat.py", "💬 Iniciando Chat Simples")


def agent():
    """Inicia o agente avançado."""
    return run_command(f"{sys.executable} src/agent.py", "🤖 Iniciando Agente Avançado")


def logs():
    """Exibe os logs."""
    print("\n📊 Logs disponíveis:")
    print("\n1. ingest.log:")
    if Path("ingest.log").exists():
        print("-" * 60)
        subprocess.run("tail -20 ingest.log", shell=True)
    else:
        print("  (vazio)")
    
    print("\n2. agent.log:")
    if Path("agent.log").exists():
        print("-" * 60)
        subprocess.run("tail -20 agent.log", shell=True)
    else:
        print("  (vazio)")
    
    print("\n3. Docker logs:")
    print("-" * 60)
    subprocess.run("docker logs postgres_rag --tail 20", shell=True)
    
    return True


def status():
    """Exibe o status do sistema."""
    print("\n📊 Status do Sistema\n")
    
    # Docker
    print("🐳 Docker Containers:")
    subprocess.run("docker ps --filter name=postgres_rag", shell=True)
    
    # Arquivo .env
    print("\n📋 Configuração (.env):")
    if Path(".env").exists():
        print("  ✓ Arquivo .env existe")
    else:
        print("  ✗ Arquivo .env NÃO existe")
    
    # Logs
    print("\n📝 Logs:")
    for log_file in ["ingest.log", "agent.log"]:
        if Path(log_file).exists():
            size = Path(log_file).stat().st_size
            print(f"  ✓ {log_file} ({size} bytes)")
        else:
            print(f"  - {log_file} (não existe)")
    
    # Ambiente virtual
    print("\n🐍 Ambiente Virtual:")
    if Path("venv").exists():
        print("  ✓ venv/ existe")
    else:
        print("  ✗ venv/ NÃO existe")
    
    return True


def clean():
    """Limpa logs e caches."""
    print("\n🧹 Limpando arquivos temporários...\n")
    
    files_to_clean = [
        "ingest.log",
        "agent.log",
        "src/__pycache__",
        "__pycache__"
    ]
    
    for file in files_to_clean:
        path = Path(file)
        if path.exists():
            if path.is_dir():
                subprocess.run(f"rm -rf {file}", shell=True)
                print(f"  ✓ Removido diretório: {file}")
            else:
                path.unlink()
                print(f"  ✓ Removido arquivo: {file}")
        else:
            print(f"  - {file} (não existe)")
    
    print("\n✅ Limpeza concluída!")
    return True


def main():
    """Função principal."""
    parser = argparse.ArgumentParser(
        description="Gerenciador do Sistema RAG",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Comandos disponíveis:
  setup      - Setup completo do sistema
  validate   - Validar configuração do ambiente
  start      - Iniciar PostgreSQL
  stop       - Parar PostgreSQL
  ingest     - Ingerir documento PDF
  chat       - Iniciar chat simples
  agent      - Iniciar agente avançado
  logs       - Exibir logs do sistema
  status     - Exibir status do sistema
  clean      - Limpar logs e caches

Exemplos:
  python manage.py setup
  python manage.py validate
  python manage.py ingest
  python manage.py agent
        """
    )
    
    parser.add_argument(
        'command',
        choices=[
            'setup', 'validate', 'start', 'stop',
            'ingest', 'chat', 'agent', 'logs',
            'status', 'clean'
        ],
        help='Comando a executar'
    )
    
    if len(sys.argv) == 1:
        parser.print_help()
        return 0
    
    args = parser.parse_args()
    
    # Mapeamento de comandos
    commands = {
        'setup': setup,
        'validate': validate,
        'start': start_db,
        'stop': stop_db,
        'ingest': ingest,
        'chat': chat,
        'agent': agent,
        'logs': logs,
        'status': status,
        'clean': clean,
    }
    
    # Executar comando
    func = commands.get(args.command)
    if func:
        success = func()
        return 0 if success else 1
    else:
        print(f"❌ Comando desconhecido: {args.command}")
        return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrompido pelo usuário")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        sys.exit(1)
