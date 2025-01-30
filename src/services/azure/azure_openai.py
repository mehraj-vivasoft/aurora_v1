from dotenv import load_dotenv
import os
from langchain_core.messages import BaseMessage
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain.schema.messages import SystemMessage, HumanMessage
from src.services.azure.ai_search import get_vector_store

def get_azure_chat_openai() -> AzureChatOpenAI:
    """Create an Azure ChatOpenAI model instance."""
    load_dotenv()

    AZURE_ENDPOINT = os.getenv("CHAT_AZURE_OPENAI_ENDPOINT")
    AZURE_API_KEY = os.getenv("CHAT_AZURE_OPENAI_API_KEY")
    AZURE_API_VERSION = os.getenv("CHAT_AZURE_OPENAI_API_VERSION")
    AZURE_DEPLOYMENT_NAME = os.getenv("CHAT_AZURE_OPENAI_DEPLOYMENT")
    
    print(AZURE_API_KEY)
    
    return AzureChatOpenAI(
        azure_deployment=AZURE_DEPLOYMENT_NAME,
        azure_endpoint=AZURE_ENDPOINT,
        openai_api_version=AZURE_API_VERSION,
        openai_api_key=AZURE_API_KEY,
        temperature=0.5,
    )

def create_rag_chain(context: str, question: str) -> BaseMessage:
    """Create a RAG chain with a prompt template."""
    # Create the base chat model
    llm = get_azure_chat_openai()        
    
    # Create messages in the correct format
    messages = [
        ("system", """You are a medical trial research assistant. 
        Provide an accurate answer based on the following context."""),
        ("human", f"""Background Context:
        {context}

        Give me a proper answer based on the above context.
        My Question: {question}
        """)
    ]
    
    # print(messages[:50] + "...")
    # print("\n"*7)  
    
    # return llm.invoke(input=messages)
    return llm.invoke(input=messages)

def run_query(query):
    
    
    # Initialize vector store
    vec_store = get_vector_store()
    
    # Example questions
    questions = [query]
    
    # Run the queries
    for question in questions:
        try:
            # Perform similarity search
            res = vec_store.similarity_search(
                query=question, k=10, search_type="hybrid"
            )
            
            # Combine context from retrieved documents
            context = "\n\n".join([doc.page_content for doc in res])
            
            response = create_rag_chain(context, question)
            
            # # Invoke the RAG chain
            # response = rag_chain.invoke({
            #     "question": question,
            #     "context": context
            # })
            
            # Print results
            print(f"Question: {question}")
            print(f"Context: {context[:80]}...")  # Truncated for readability
            print(f"Response: {response.content}\n")
            
            return response.content
        
        except Exception as e:
            print(f"Error processing question '{question}': {e}")