import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_postgres import PGVector

load_dotenv()

PROMPT_TEMPLATE = """
CONTEXTO:
{context}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{question}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""

CONNECTION_STRING = os.getenv("CONNECTION_STRING", "postgresql+psycopg2://postgres:postgres@localhost:5432/rag")
COLLECTION_NAME = "document_vectors"

def search(question: str):
    """
    Performs a similarity search in the database and returns the answer from the LLM.
    """
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001"
    )
    store = PGVector(
        collection_name=COLLECTION_NAME,
        connection=CONNECTION_STRING,
        embedding_function=embeddings,
    )
    retriever = store.as_retriever(search_kwargs={"k": 10})

    prompt = PromptTemplate(
        template=PROMPT_TEMPLATE,
        input_variables=["context", "question"],
    )

    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash", temperature=0
    )

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
    )

    return rag_chain.invoke(question)


if __name__ == '__main__':
    # Example of how to use the function
    result = search("Qual o faturamento da Empresa SuperTechIABrazil?")
    print(result.content)