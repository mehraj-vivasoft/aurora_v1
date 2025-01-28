from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from langchain_community.vectorstores.azuresearch import AzureSearch
from langchain_openai import AzureOpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from langchain_core.documents import Document

load_dotenv()

connection_string = (
    f"mssql+pyodbc://{os.getenv('SQL_USERNAME')}:{os.getenv('SQL_PASSWORD')}@"
    f"{os.getenv('SQL_SERVER')}/"
    f"{os.getenv('SQL_DATABASE')}?driver={os.getenv('ODBCDRIVER')}"
)

engine = create_engine(connection_string)
db = SQLDatabase(engine=engine)

# Query to select all columns from HTA table
query = """
SELECT TOP 2 
    ID,
    HTA_AGENCY_NAME,
    COUNTRY,
    HTA_DECISION_DT,
    BIOMARKERS,
    PRIMARY_DISEASE,
    DRUG_NAME,
    GENERIC_DRUG_NAME,
    DRUG_COMBINATIONS,
    GENERAL_HTA_CONCLUSION,
    DOSING,
    TREATMENT_DURATION,
    INTERVENTION_ADD_DETAILS,
    TREATMENT_LINE,
    TREATMENT_MODALITY,
    COMPARATOR_DRUGS,
    COMPARATOR_COMBINATION_THERAPY,
    COMPARATOR_DRUGS_PAYERS,
    COMPARATOR_ADD_DETAILS,
    TARGET_POPULATION,
    ASMR_REQUESTED,
    ASMR_RECIEVED,
    CLINICAL_OUTCOMES,
    DATA_PACKAGES,
    STUDY_TYPE,
    EVENDENCE_SYNTHESIS,
    OUTCOMES_FROM_EVIDENCE,
    COA_INSTRUMENTS,
    COA_TYPE,
    COA_DETAILS,
    RWE_USED,
    RWE_DATA_TYPE,
    RWE_PAYER_ACCEPTED,
    HTA_ANALYSIS_TYPE,
    CEA_EFFECTIVENESS_MEASURE,
    ECON_MODEL,
    TIME_HORIZON,
    ECON_MODEL_DESIGN,
    PAYER_DECISION,
    KEY_DRIVE_CE,
    CLINICAL_POSITIVES,
    CLINICAL_NEGATIVES,
    FINAL_RECOMMENDATION,
    SUBGROUP_NAME,
    HTA_STATUS,
    QUINTILES_LINK,
    WEB_URL,
    REIMBURSED_INDICATION,
    RWE_DETAILS
FROM dbo.HTA
"""

results = db.run(query)
# print("\nRaw SQL Results:")
# print(results)

# Convert SQL results to documents
documents = []
for row in results.split('\n'):
    if row.strip():  # Skip empty lines
        # Create a more structured document with metadata
        doc = Document(
            page_content=row,
            metadata={
                "source": "HTA Database",
                "row_number": len(documents) + 1
            }
        )
        documents.append(doc)

print("\nProcessed Documents:")
for doc in documents:
    print(f"\nDocument {doc.metadata['row_number']}:")
    print(doc.page_content)

azure_endpoint: str = os.getenv("AZURE_OPENAI_ENDPOINT")
azure_openai_api_key: str = os.getenv("AZURE_OPENAI_API_KEY")
azure_openai_api_version: str = os.getenv("AZURE_OPENAI_API_VERSION")
azure_deployment: str = os.getenv("AZURE_OPENAI_DEPLOYMENT")

vector_store_address: str = os.getenv("AZURE_SEARCH_ENDPOINT")
vector_store_password: str = os.getenv("AZURE_SEARCH_ADMIN_KEY")

embeddings: AzureOpenAIEmbeddings = AzureOpenAIEmbeddings(
    azure_deployment=azure_deployment,
    openai_api_version=azure_openai_api_version,
    azure_endpoint=azure_endpoint,
    api_key=azure_openai_api_key,
)

index_name: str = "hta-vector-store"
vector_store: AzureSearch = AzureSearch(
    azure_search_endpoint=vector_store_address,
    azure_search_key=vector_store_password,
    index_name=index_name,
    embedding_function=embeddings.embed_query,
    additional_search_client_options={"retry_total": 4},
)

text_splitter = CharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    separator="\n"
)
docs = text_splitter.split_documents(documents)

print(f"\nNumber of chunks after splitting: {len(docs)}")
print("\nChunked Documents:")
for i, doc in enumerate(docs):
    print(f"\nChunk {i+1}:")
    print(doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content)

vector_store.add_documents(docs)
print("\nDocuments added to vector store")

# Example queries
example_queries = [
    "What are the clinical outcomes for the HTA?",
    "What are the drug combinations used?",
    "What are the primary diseases treated?",
    "What are the biomarkers mentioned?",
]

print("\nRunning example queries:")
for query in example_queries:
    print(f"\nQuery: {query}")
    results = vector_store.similarity_search(query, k=2)  # Get top 2 results
    print("Results:")
    for i, doc in enumerate(results):
        print(f"\nResult {i+1}:")
        print(doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content)  # noqa: E501
