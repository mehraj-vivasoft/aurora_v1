from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from langchain_community.vectorstores.azuresearch import AzureSearch
from langchain_openai import AzureOpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from langchain_core.documents import Document

load_dotenv()

azure_endpoint: str = os.getenv("AZURE_OPENAI_ENDPOINT")
azure_openai_api_key: str = os.getenv("AZURE_OPENAI_API_KEY")
azure_openai_api_version: str = os.getenv("AZURE_OPENAI_API_VERSION")
azure_deployment: str = os.getenv("AZURE_OPENAI_DEPLOYMENT")

vector_store_address: str = os.getenv("AZURE_SEARCH_ENDPOINT")
vector_store_password: str = os.getenv("AZURE_SEARCH_ADMIN_KEY")


def connect_to_db():
    connection_string = (
        f"mssql+pyodbc://{os.getenv('SQL_USERNAME')}:{os.getenv('SQL_PASSWORD')}@"  # noqa: E501
        f"{os.getenv('SQL_SERVER')}/"
        f"{os.getenv('SQL_DATABASE')}?driver={os.getenv('ODBCDRIVER')}"
    )

    engine = create_engine(connection_string)
    db = SQLDatabase(engine=engine)

    return db


def get_entries():
    db = connect_to_db()

    query = "SELECT TOP (10) CLINICAL_OUTCOMES FROM dbo.HTA"
    results = db.run(query)
    print(results)

    return results


def convert_to_documents():

    results = get_entries()

    documents = []
    for row in results.split('\n'):
        if row.strip():
            documents.append(Document(page_content=row))

    return documents


def get_embedder():
    embeddings: AzureOpenAIEmbeddings = AzureOpenAIEmbeddings(
        azure_deployment=azure_deployment,
        openai_api_version=azure_openai_api_version,
        azure_endpoint=azure_endpoint,
        api_key=azure_openai_api_key,
    )
    return embeddings


def get_vector_store(embeddings):
    index_name: str = "langchain-vector-demo"
    # Specify additional properties for the Azure client such as the following https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/core/azure-core/README.md#configurations # noqa: E501
    vector_store: AzureSearch = AzureSearch(
        azure_search_endpoint=vector_store_address,
        embedding_function=embeddings.embed_query,
        azure_search_key=vector_store_password,
        index_name=index_name,
        # Configure max retries for the Azure client
        additional_search_client_options={"retry_total": 4},
    )
    return vector_store


def get_text_splitter():
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    return text_splitter


def add_documents(vector_store, documents):
    documents = convert_to_documents()
    text_splitter = get_text_splitter()
    docs = text_splitter.split_documents(documents)
    embeddings = get_embedder()
    vector_store = get_vector_store(embeddings)

    vector_store.add_documents(docs)

    return vector_store


if __name__ == "__main__":
    res = convert_to_documents()
    print(res)
