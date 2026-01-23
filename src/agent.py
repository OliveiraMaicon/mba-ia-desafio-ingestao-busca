"""
Agente de IA Avançado com RAG, Memory e Tools

Este módulo implementa um agente de IA sofisticado que combina:
- RAG (Retrieval Augmented Generation) para busca semântica
- Memory para manter contexto de conversação
- Tools customizadas para funcionalidades expandidas
- Capacidade de reasoning e multi-step planning
"""

import os
import sys
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_postgres import PGVector
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.tools import Tool
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('agent.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

load_dotenv()

# Configurações
CONNECTION_STRING = os.getenv("CONNECTION_STRING", "postgresql+psycopg://postgres:postgres@localhost:5432/rag")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "document_vectors")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "models/embedding-001")
LLM_MODEL = os.getenv("LLM_MODEL", "gemini-1.5-flash")
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.3"))
SEARCH_K = int(os.getenv("SEARCH_K", "10"))

# Armazenamento de histórico de conversas por session_id
store = {}


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    """Recupera ou cria histórico de conversa para uma sessão."""
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]


class RAGAgent:
    """Agente de IA avançado com RAG, memory e tools customizadas."""
    
    def __init__(self, session_id: str = "default"):
        """
        Inicializa o agente.
        
        Args:
            session_id: ID da sessão para manter histórico de conversação
        """
        self.session_id = session_id
        logger.info(f"Inicializando RAGAgent (session: {session_id})")
        
        # Configurar embeddings
        self.embeddings = GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL)
        
        # Configurar vector store
        self.vector_store = PGVector(
            collection_name=COLLECTION_NAME,
            connection=CONNECTION_STRING,
            embeddings=self.embeddings,
        )
        
        # Configurar LLM
        self.llm = ChatGoogleGenerativeAI(
            model=LLM_MODEL,
            temperature=TEMPERATURE
        )
        
        # Criar tools
        self.tools = self._create_tools()
        
        # Criar agent
        self.agent_executor = self._create_agent()
        
        logger.info("RAGAgent inicializado com sucesso")
    
    def _create_tools(self) -> List[Tool]:
        """Cria as tools disponíveis para o agente."""
        
        def search_documents(query: str) -> str:
            """Busca informações relevantes no documento ingerido."""
            try:
                logger.info(f"Tool search_documents chamada com query: {query[:100]}")
                retriever = self.vector_store.as_retriever(search_kwargs={"k": SEARCH_K})
                docs = retriever.get_relevant_documents(query)
                
                if not docs:
                    return "Nenhum documento relevante encontrado para a consulta."
                
                # Formatar resultados
                result = f"Encontrados {len(docs)} documentos relevantes:\n\n"
                for i, doc in enumerate(docs, 1):
                    result += f"[Documento {i}]\n{doc.page_content}\n\n"
                
                logger.info(f"Tool retornou {len(docs)} documentos")
                return result
                
            except Exception as e:
                logger.error(f"Erro na tool search_documents: {e}")
                return f"Erro ao buscar documentos: {str(e)}"
        
        def get_current_datetime() -> str:
            """Retorna a data e hora atual."""
            now = datetime.now()
            return f"Data e hora atual: {now.strftime('%d/%m/%Y %H:%M:%S')}"
        
        def summarize_conversation() -> str:
            """Resume a conversa atual."""
            try:
                history = get_session_history(self.session_id)
                messages = history.messages
                
                if not messages:
                    return "Nenhuma conversa anterior encontrada."
                
                summary = f"Resumo da conversa ({len(messages)} mensagens):\n\n"
                for i, msg in enumerate(messages[-10:], 1):  # Últimas 10 mensagens
                    role = "Usuário" if isinstance(msg, HumanMessage) else "Assistente"
                    content = msg.content[:100] + "..." if len(msg.content) > 100 else msg.content
                    summary += f"{i}. {role}: {content}\n"
                
                return summary
                
            except Exception as e:
                logger.error(f"Erro ao resumir conversa: {e}")
                return f"Erro ao resumir conversa: {str(e)}"
        
        def calculate(expression: str) -> str:
            """
            Calcula expressões matemáticas simples.
            Exemplo: "2 + 2" retorna "4"
            """
            try:
                # Segurança: apenas operações básicas
                allowed_chars = set("0123456789+-*/()., ")
                if not all(c in allowed_chars for c in expression):
                    return "Erro: Expressão contém caracteres não permitidos"
                
                result = eval(expression, {"__builtins__": {}}, {})
                return f"Resultado: {result}"
                
            except Exception as e:
                logger.error(f"Erro ao calcular: {e}")
                return f"Erro ao calcular expressão: {str(e)}"
        
        # Definir tools
        tools = [
            Tool(
                name="search_documents",
                func=search_documents,
                description=(
                    "Busca informações relevantes no documento PDF ingerido. "
                    "Use esta ferramenta quando precisar responder perguntas sobre o conteúdo do documento. "
                    "Input deve ser uma pergunta ou query de busca."
                )
            ),
            Tool(
                name="get_datetime",
                func=get_current_datetime,
                description=(
                    "Retorna a data e hora atual. "
                    "Use quando o usuário perguntar sobre data, hora ou informações temporais."
                )
            ),
            Tool(
                name="summarize_conversation",
                func=summarize_conversation,
                description=(
                    "Resume o histórico da conversa atual. "
                    "Use quando o usuário pedir um resumo ou contexto da conversa."
                )
            ),
            Tool(
                name="calculate",
                func=calculate,
                description=(
                    "Calcula expressões matemáticas simples. "
                    "Suporta +, -, *, /, (), números decimais. "
                    "Exemplo de input: '(10 + 5) * 2'"
                )
            ),
        ]
        
        logger.info(f"Criadas {len(tools)} tools: {[t.name for t in tools]}")
        return tools
    
    def _create_agent(self) -> AgentExecutor:
        """Cria o agent executor com tools e memory."""
        
        # Prompt do sistema
        system_prompt = """Você é um assistente de IA avançado especializado em responder perguntas sobre documentos.

INSTRUÇÕES:
1. Quando o usuário fizer uma pergunta sobre o documento, use a ferramenta "search_documents"
2. SEMPRE busque informações no documento antes de responder
3. Base suas respostas APENAS nas informações encontradas
4. Se a informação não estiver no documento, diga claramente: "Não tenho informações necessárias para responder sua pergunta."
5. Mantenha o contexto da conversa usando o histórico
6. Use outras ferramentas quando apropriado (data/hora, cálculos, etc.)
7. Seja conciso, preciso e útil
8. Se precisar de mais informações, peça ao usuário

IMPORTANTE: Nunca invente informações ou use conhecimento externo ao documento."""
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        # Criar agent
        agent = create_tool_calling_agent(self.llm, self.tools, prompt)
        
        # Criar executor
        agent_executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=5,
        )
        
        # Adicionar memory
        agent_with_memory = RunnableWithMessageHistory(
            agent_executor,
            get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
        )
        
        return agent_with_memory
    
    def chat(self, message: str) -> str:
        """
        Envia uma mensagem para o agente e retorna a resposta.
        
        Args:
            message: Mensagem do usuário
            
        Returns:
            Resposta do agente
        """
        try:
            if not message or not message.strip():
                return "Por favor, faça uma pergunta."
            
            logger.info(f"Processando mensagem: {message[:100]}")
            
            # Invocar agent com histórico
            response = self.agent_executor.invoke(
                {"input": message},
                config={"configurable": {"session_id": self.session_id}}
            )
            
            output = response.get("output", "Desculpe, não consegui processar sua pergunta.")
            logger.info(f"Resposta gerada com sucesso")
            
            return output
            
        except Exception as e:
            logger.exception(f"Erro ao processar chat: {e}")
            return f"Erro ao processar mensagem: {str(e)}"
    
    def clear_history(self):
        """Limpa o histórico da conversa."""
        if self.session_id in store:
            del store[self.session_id]
            store[self.session_id] = ChatMessageHistory()
            logger.info(f"Histórico limpo para session {self.session_id}")
    
    def get_history(self) -> List[Dict[str, str]]:
        """Retorna o histórico de mensagens da sessão."""
        history = get_session_history(self.session_id)
        return [
            {
                "role": "user" if isinstance(msg, HumanMessage) else "assistant",
                "content": msg.content
            }
            for msg in history.messages
        ]


def main():
    """Interface de chat interativa com o agente avançado."""
    print("=" * 70)
    print("  🤖 AGENTE DE IA AVANÇADO - RAG com Memory e Tools")
    print("=" * 70)
    print("\nRecursos disponíveis:")
    print("  ✓ Busca semântica no documento")
    print("  ✓ Memória de conversação")
    print("  ✓ Ferramentas customizadas (data/hora, cálculos, resumos)")
    print("  ✓ Multi-step reasoning")
    print("\nComandos:")
    print("  'sair' - Encerrar")
    print("  'limpar' - Limpar histórico")
    print("  'historico' - Ver histórico")
    print("  'ajuda' - Mostrar ajuda")
    print()
    
    # Criar agente
    try:
        agent = RAGAgent(session_id=f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
    except Exception as e:
        print(f"\n❌ Erro ao inicializar agente: {e}")
        print("Certifique-se de que:")
        print("  1. PostgreSQL está rodando: docker compose up -d")
        print("  2. Dados foram ingeridos: python src/ingest.py")
        print("  3. GOOGLE_API_KEY está configurada no .env")
        return
    
    question_count = 0
    
    while True:
        try:
            message = input("\n💭 Você: ").strip()
            
            if not message:
                continue
            
            # Comandos especiais
            if message.lower() in ['sair', 'exit', 'quit']:
                print("\n👋 Até logo!")
                break
            
            if message.lower() in ['limpar', 'clear']:
                agent.clear_history()
                print("✓ Histórico limpo")
                continue
            
            if message.lower() in ['historico', 'history']:
                history = agent.get_history()
                if not history:
                    print("Nenhuma conversa anterior")
                else:
                    print(f"\n📜 Histórico ({len(history)} mensagens):")
                    for i, msg in enumerate(history, 1):
                        role = "Você" if msg["role"] == "user" else "Agente"
                        print(f"{i}. {role}: {msg['content'][:100]}...")
                continue
            
            if message.lower() in ['ajuda', 'help']:
                print("\n📖 Ajuda:")
                print("  - Faça perguntas sobre o documento")
                print("  - Peça cálculos: 'calcule 10 * 5'")
                print("  - Pergunte a data/hora: 'que horas são?'")
                print("  - Peça resumos: 'resuma nossa conversa'")
                print("  - O agente mantém contexto da conversa")
                continue
            
            # Processar mensagem
            question_count += 1
            print("\n⏳ Processando...", end='', flush=True)
            
            response = agent.chat(message)
            
            print("\r" + " " * 30 + "\r", end='')
            print(f"\n🤖 Agente:")
            print("-" * 70)
            print(response)
            print("-" * 70)
            
        except KeyboardInterrupt:
            print("\n\n⚠️  Interrompido. Digite 'sair' para encerrar.")
            continue
        
        except Exception as e:
            print(f"\n❌ Erro: {e}")
            logger.exception(f"Erro no loop principal: {e}")
    
    if question_count > 0:
        print(f"\n📊 Total de perguntas: {question_count}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.exception(f"Erro fatal: {e}")
        print(f"\n❌ Erro fatal: {e}")
        sys.exit(1)
