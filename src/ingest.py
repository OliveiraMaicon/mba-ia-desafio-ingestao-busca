import os
import sys
import logging
from pathlib import Path
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_postgres import PGVector
from sqlalchemy import create_engine, text

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ingest.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

load_dotenv()

PDF_PATH = os.getenv("PDF_PATH", "document.pdf")
CONNECTION_STRING = os.getenv("CONNECTION_STRING", "postgresql+psycopg://postgres:postgres@localhost:5432/rag")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "document_vectors")
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "150"))
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "models/embedding-001")


def validate_environment():
    """Valida as variáveis de ambiente e configurações necessárias."""
    logger.info("Validando ambiente...")
    
    # Verificar GOOGLE_API_KEY
    if not os.getenv("GOOGLE_API_KEY"):
        logger.error("GOOGLE_API_KEY não configurada no arquivo .env")
        raise ValueError("GOOGLE_API_KEY não encontrada. Configure-a no arquivo .env")
    
    # Verificar se o PDF existe
    pdf_path = Path(PDF_PATH)
    if not pdf_path.exists():
        logger.error(f"Arquivo PDF não encontrado: {PDF_PATH}")
        raise FileNotFoundError(f"Arquivo PDF não encontrado: {PDF_PATH}")
    
    if not pdf_path.suffix.lower() == '.pdf':
        logger.error(f"Arquivo não é um PDF: {PDF_PATH}")
        raise ValueError(f"Arquivo deve ser PDF: {PDF_PATH}")
    
    logger.info(f"Arquivo PDF encontrado: {PDF_PATH} ({pdf_path.stat().st_size / 1024:.2f} KB)")
    
    # Testar conexão com banco de dados
    try:
        engine = create_engine(CONNECTION_STRING)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("Conexão com banco de dados OK")
    except Exception as e:
        logger.error(f"Erro ao conectar ao banco de dados: {e}")
        raise ConnectionError(f"Não foi possível conectar ao banco de dados: {e}")
    
    return True


def ingest_pdf():
    """
    Ingests a PDF file, splits it into chunks, generates embeddings, and stores them in a PostgreSQL database.
    """
    try:
        # Validar ambiente
        validate_environment()
        
        logger.info(f"Iniciando ingestão do PDF: {PDF_PATH}")
        
        # Carregar PDF
        logger.info("Carregando documento PDF...")
        loader = PyPDFLoader(PDF_PATH)
        documents = loader.load()
        logger.info(f"Documento carregado com {len(documents)} páginas")
        
        # Dividir em chunks
        logger.info(f"Dividindo documento em chunks (size={CHUNK_SIZE}, overlap={CHUNK_OVERLAP})...")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE, 
            chunk_overlap=CHUNK_OVERLAP
        )
        docs = text_splitter.split_documents(documents)
        logger.info(f"Documento dividido em {len(docs)} chunks")
        
        # Criar embeddings
        logger.info(f"Gerando embeddings com modelo {EMBEDDING_MODEL}...")
        embeddings = GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL)
        
        # Armazenar no banco
        logger.info(f"Armazenando chunks no banco de dados (collection: {COLLECTION_NAME})...")
        PGVector.from_documents(
            embedding=embeddings,
            documents=docs,
            collection_name=COLLECTION_NAME,
            connection=CONNECTION_STRING,
            pre_delete_collection=True,
        )
        
        logger.info(f"✅ Ingestão concluída com sucesso! {len(docs)} chunks armazenados.")
        print(f"\n✅ Sucesso! {len(docs)} chunks do arquivo '{PDF_PATH}' foram ingeridos no banco de dados.")
        return True
        
    except FileNotFoundError as e:
        logger.error(f"Arquivo não encontrado: {e}")
        print(f"\n❌ Erro: {e}")
        return False
    except ValueError as e:
        logger.error(f"Erro de validação: {e}")
        print(f"\n❌ Erro: {e}")
        return False
    except ConnectionError as e:
        logger.error(f"Erro de conexão: {e}")
        print(f"\n❌ Erro: {e}")
        print("Certifique-se de que o PostgreSQL está rodando: docker compose up -d")
        return False
    except Exception as e:
        logger.exception(f"Erro inesperado durante ingestão: {e}")
        print(f"\n❌ Erro inesperado: {e}")
        return False


if __name__ == "__main__":
    success = ingest_pdf()
    sys.exit(0 if success else 1)