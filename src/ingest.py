import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_postgres import PGVector

load_dotenv()

PDF_PATH = os.getenv("PDF_PATH", "document.pdf")
CONNECTION_STRING = os.getenv("CONNECTION_STRING", "postgresql+psycopg2://postgres:postgres@localhost:5432/rag")
COLLECTION_NAME = "document_vectors"

def ingest_pdf():
    """
    Ingests a PDF file, splits it into chunks, generates embeddings, and stores them in a PostgreSQL database.
    """
    loader = PyPDFLoader(PDF_PATH)
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    docs = text_splitter.split_documents(documents)

    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    PGVector.from_documents(
        embedding=embeddings,
        documents=docs,
        collection_name=COLLECTION_NAME,
        connection=CONNECTION_STRING,
        pre_delete_collection=True,
    )
    print(f"Successfully ingested {len(docs)} chunks from {PDF_PATH}")


if __name__ == "__main__":
    ingest_pdf()