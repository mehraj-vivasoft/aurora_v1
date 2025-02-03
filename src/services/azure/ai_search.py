from dotenv import load_dotenv
import os
from langchain_community.vectorstores.azuresearch import AzureSearch
from langchain_core import embeddings
from langchain_openai import AzureOpenAIEmbeddings
from azure.search.documents.indexes.models import (
    SearchableField,
    SearchField,
    SearchFieldDataType,
    SimpleField,
)


def get_embedder(azure_deployment,azure_openai_api_version,azure_endpoint,azure_openai_api_key):
    embeddings: AzureOpenAIEmbeddings = AzureOpenAIEmbeddings(
        azure_deployment=azure_deployment,
        openai_api_version=azure_openai_api_version,
        azure_endpoint=azure_endpoint,
        api_key=azure_openai_api_key,
    )
    return embeddings


def get_vector_store() -> AzureSearch:
    load_dotenv()

    azure_endpoint: str = os.getenv("AZURE_OPENAI_ENDPOINT")
    azure_openai_api_key: str = os.getenv("AZURE_OPENAI_API_KEY")
    azure_openai_api_version: str = os.getenv("AZURE_OPENAI_API_VERSION")
    azure_deployment: str = os.getenv("AZURE_OPENAI_DEPLOYMENT")
    
    embedding_function = get_embedder(azure_deployment,azure_openai_api_version,azure_endpoint,azure_openai_api_key).embed_query

    vector_store_address: str = os.getenv("AZURE_SEARCH_ENDPOINT")
    vector_store_password: str = os.getenv("AZURE_SEARCH_ADMIN_KEY")
    
    fields = [
        SimpleField(
            name="id",
            type=SearchFieldDataType.String,
            key=True,
            filterable=True,
        ),
        SearchableField(
            name="content",
            type=SearchFieldDataType.String,
            searchable=True,
        ),
        SearchField(
            name="content_vector",
            type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
            searchable=True,
            vector_search_dimensions=len(embedding_function("Text")),
            vector_search_profile_name="myHnswProfile",
        ),        
        SimpleField(
            name="entry_id",
            type=SearchFieldDataType.String,
            filterable=True,
        ),
        SearchField(
            name="metadata",
            type=SearchFieldDataType.String,
            filterable=True,
        )
    ]
    
    index_name: str = "processed-index-v2"
    # Specify additional properties for the Azure client such as the following https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/core/azure-core/README.md#configurations # noqa: E501
    vector_store: AzureSearch = AzureSearch(
        azure_search_endpoint=vector_store_address,
        embedding_function=embedding_function,
        azure_search_key=vector_store_password,
        index_name=index_name,
        fields=fields,
        # Configure max retries for the Azure client
        additional_search_client_options={"retry_total": 4},
    )
    
    return vector_store