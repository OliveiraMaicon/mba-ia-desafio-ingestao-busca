import sys
import logging
from search import search

# Configurar logging
logging.basicConfig(
    level=logging.WARNING,  # Menos verboso no chat
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Interface de chat interativa para fazer perguntas sobre o documento."""
    print("=" * 60)
    print("  BEM-VINDO AO CHAT RAG - Sistema de Busca Semântica")
    print("=" * 60)
    print("\nFaça perguntas sobre o documento ingerido.")
    print("Digite 'sair', 'exit' ou 'quit' para terminar.")
    print("Digite 'ajuda' para ver comandos disponíveis.\n")
    
    question_count = 0
    
    while True:
        try:
            # Ler pergunta do usuário
            question = input("\n💭 Sua pergunta: ").strip()
            
            # Comandos especiais
            if not question:
                continue
                
            if question.lower() in ['sair', 'exit', 'quit', 'q']:
                print("\n👋 Até logo!")
                break
                
            if question.lower() in ['ajuda', 'help', '?']:
                print("\n📖 Comandos disponíveis:")
                print("  - Digite uma pergunta para buscar informações")
                print("  - 'sair', 'exit', 'quit' - Encerrar o chat")
                print("  - 'ajuda', 'help' - Mostrar esta mensagem")
                print("  - 'limpar', 'clear' - Limpar a tela")
                continue
                
            if question.lower() in ['limpar', 'clear', 'cls']:
                print("\033[2J\033[H")  # Limpar terminal
                continue
            
            # Processar pergunta
            question_count += 1
            logger.info(f"Processando pergunta #{question_count}: {question[:50]}...")
            
            print("\n⏳ Buscando resposta...", end='', flush=True)
            response = search(question)
            print("\r" + " " * 30 + "\r", end='')  # Limpar linha
            
            # Exibir resposta
            print(f"\n🤖 Resposta:")
            print("-" * 60)
            print(response.content)
            print("-" * 60)
            
        except KeyboardInterrupt:
            print("\n\n⚠️  Interrompido pelo usuário. Digite 'sair' para encerrar.")
            continue
            
        except ValueError as e:
            print(f"\n❌ Erro: {e}")
            logger.error(f"Erro de validação: {e}")
            
        except ConnectionError as e:
            print(f"\n❌ Erro de conexão: {e}")
            print("Certifique-se de que:")
            print("  1. O PostgreSQL está rodando: docker compose up -d")
            print("  2. Os dados foram ingeridos: python src/ingest.py")
            logger.error(f"Erro de conexão: {e}")
            
        except Exception as e:
            print(f"\n❌ Erro inesperado: {e}")
            logger.exception(f"Erro inesperado: {e}")
            print("\nTente novamente ou digite 'sair' para encerrar.")
    
    # Estatísticas finais
    if question_count > 0:
        print(f"\n📊 Total de perguntas processadas: {question_count}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.exception(f"Erro fatal no chat: {e}")
        print(f"\n❌ Erro fatal: {e}")
        sys.exit(1)