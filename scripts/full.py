import logging
from typing import List, Optional
from sqlalchemy import create_engine, text
# from langchain_community.utilities import SQLDatabase
from langchain_openai import AzureOpenAIEmbeddings
from langchain_community.vectorstores import AzureSearch
from langchain_core.documents import Document

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def import_sqldb_to_azure_search(
    sqldb_connection_string: str,
    azure_openai_endpoint: str,
    azure_openai_key: str,
    azure_search_endpoint: str,
    azure_search_key: str,
    query: str,
    index_name: str = "sqldb-imported-index",
    batch_size: int = 100,
    text_column: Optional[str] = None,
    metadata_columns: Optional[List[str]] = None
):
    """
    Import data from Azure SQL Database to Azure AI Search with advanced configuration. # noqa: E501
    
    Args:
        sqldb_connection_string (str): Connection string for Azure SQL Database
        azure_openai_endpoint (str): Azure OpenAI endpoint
        azure_openai_key (str): Azure OpenAI API key
        azure_search_endpoint (str): Azure AI Search endpoint
        azure_search_key (str): Azure AI Search admin key
        query (str): SQL query to fetch data
        index_name (str, optional): Name of the Azure AI Search index
        batch_size (int, optional): Number of documents to process in each batch # noqa: E501
        text_column (str, optional): Specific column to use as document text
        metadata_columns (List[str], optional): Columns to include as metadata
    """
    try:
        # 1. Connect to SQL Database
        logger.info("Connecting to Azure SQL Database...")
        engine = create_engine(sqldb_connection_string)
        # db = SQLDatabase(engine=engine)

        # 2. Execute Query with SQLAlchemy for better safety
        logger.info(f"Executing query: {query}")
        with engine.connect() as connection:
            result = connection.execute(text(query))
            rows = result.fetchall()
            column_names = result.keys()

        logger.info(f"Retrieved {len(rows)} rows from database")

        # 3. Configure Embeddings
        logger.info("Configuring Azure OpenAI Embeddings...")
        embeddings = AzureOpenAIEmbeddings(
            azure_deployment="text-embedding-ada-002",
            azure_endpoint=azure_openai_endpoint,
            openai_api_version="2023-05-15",
            openai_api_key=azure_openai_key
        )

        # 4. Create Azure AI Search Vector Store
        logger.info(f"Creating Azure AI Search index: {index_name}")
        vector_store = AzureSearch(
            azure_search_endpoint=azure_search_endpoint,
            azure_search_key=azure_search_key,
            index_name=index_name,
            embedding_function=embeddings.embed_query
        )

        # 5. Transform and Add Documents in Batches
        documents = []
        for row in rows:
            # Convert row to dictionary
            row_dict = dict(zip(column_names, row))

            # Determine text content
            if text_column:
                page_content = str(row_dict.get(text_column, ''))
            else:
                # If no specific column, use first text-like column
                page_content = next(
                    (str(val) for val in row_dict.values() if isinstance(val, str)),  # noqa: E501
                    str(row_dict)
                )

            # Prepare metadata
            metadata = {
                "source": "azure_sqldb",
                "index_name": index_name
            }

            # Add specified metadata columns
            if metadata_columns:
                for col in metadata_columns:
                    if col in row_dict:
                        metadata[col] = str(row_dict[col])
                        # Create document
            document = Document(
                page_content=page_content,
                metadata=metadata
            )
            documents.append(document)

            # Add documents in batches
            if len(documents) >= batch_size:
                vector_store.add_documents(documents)
                documents = []

        # Add remaining documents
        if documents:
            vector_store.add_documents(documents)

        logger.info("Successfully imported data to Azure AI Search index")
    except Exception as e:
        logger.error(f"Error importing data: {e}")
        raise e
