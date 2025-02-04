from fastapi import BackgroundTasks
from src.services.load.templates.large_docs import get_large_docs
from src.services.load.templates.merged_docs import get_merged_docs
from src.services.load.get_unprocessed import get_unprocessed_docs
from src.services.azure.ai_search import get_vector_store

def load_unprocessed_data(file_name: str, index_name: str = "processed-index-v2"):
    
    hta_docs = get_unprocessed_docs(file_name)
    vec_store = get_vector_store(index_name=index_name)
    
    print(len(hta_docs.records), " records found for file ", file_name)
    
    for record in hta_docs.records:
        large_docs = get_large_docs(record)
        merged_docs = get_merged_docs(record)
        doc = merged_docs + large_docs

        res = vec_store.add_documents(doc, additional_fields={"entry_id": record.id})

        # print("vector store ids : ", res)
        print(len(doc), " documents added to vector store for id ", record.id)


async def load_unprocessed_data_in_background(file_name: str, index_name: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(load_unprocessed_data, file_name, index_name)
    return "Started loading unprocessed data from " + file_name