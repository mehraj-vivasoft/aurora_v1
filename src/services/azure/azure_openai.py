from dotenv import load_dotenv
import os
from langchain_core.messages import BaseMessage
from langchain_openai import AzureChatOpenAI
from typing import Iterator, Union
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

def create_rag_chain(context: str, question: str, stream: bool = False, prev_messages: list[str] = []):
    """Create a RAG chain with a prompt template."""
    
    llm = get_azure_chat_openai()
    
    prev_msg_data = ""
    
    if len(prev_messages) > 0:
        prev_msg_data = """I asked this previous question:
        {prev_messages}
        """
        
    messages = [
        ("system", """You are a medical trial research assistant. 
        Provide an accurate answer based on the following context."""),
        ("human", f"""Background Context:
        {context}

        Give me a proper answer based on the above context.
        My Question: {question}
        """)
    ]
        
    if stream:
        return llm.stream(input=messages)
    else:
        return llm.invoke(input=messages)

def run_query(query, filtered_ids = [], prev_messages=[]):
    
    filter_str = " or ".join([f"entry_id eq '{id}'" for id in filtered_ids])
    print(filter_str)
    
    vec_store = get_vector_store()    
    questions = [query]
        
    for question in questions:
        try:            
            res = vec_store.similarity_search(
                query=question, k=10, search_type="hybrid", filters=filter_str
            )
            
            context = "\n\n".join([doc.page_content for doc in res])
            
            response = create_rag_chain(context, question, stream=False, prev_messages=prev_messages)                        
            
            print(res)
                        
            print(f"Question: {question}")
            print(f"Context: {context[:80]}...")  # Truncated for readability
            print(f"Response: {response.content}\n")
            
            return response.content
        
        except Exception as e:
            print(f"Error processing question '{question}': {e}")
            
def run_stream(query, filtered_ids = [], prev_messages=[]):
    
    filter_str = " or ".join([f"entry_id eq '{id}'" for id in filtered_ids])
    print(filter_str)
    
    vec_store = get_vector_store()    
    questions = [query]
        
    for question in questions:
        try:            
            res = vec_store.similarity_search(
                query=question, k=10, search_type="hybrid", filters=filter_str
            )
            
            context = "\n\n".join([doc.page_content for doc in res])
            
            response = create_rag_chain(context, question, stream=True, prev_messages=prev_messages)
            
            
            try:
                for chunk in response:
                    if chunk.content:
                        yield chunk.content.encode("utf-8")
            except Exception as e:
                print(f"Error in streaming '{question}': {e}")
                yield "error : " + str(e)
                                        
        
        except Exception as e:
            print(f"Error processing question '{question}': {e}")