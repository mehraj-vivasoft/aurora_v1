from scripts.final.get_hta_records import get_hta_records
from scripts.templates.merged_docs import get_merged_docs
from scripts.templates.large_docs import get_large_docs

from src.services.azure.ai_search import get_vector_store
from src.services.azure.azure_openai import run_query

if __name__ == "__main__":
    hta_records = get_hta_records()
    print(len(hta_records.records), " records found")
    separator = "_" * 400
    vec_store = get_vector_store()

    with open("hta_docs.txt", "w", encoding="utf-8") as file:
        for record in hta_records.records:
            large_docs = get_large_docs(record)
            merged_docs = get_merged_docs(record)
            doc = merged_docs + large_docs

            res = vec_store.add_documents(doc, additional_fields={"entry_id": record.id})
            
            print("result : ", res)
            
            print(len(doc), " documents added to vector store for id ", record.id)
            
            for page in doc:                
                file.write(page.page_content + "\nMetadata:" + str(page.metadata) + f"\n{separator}\n")
    
    print("Documents saved to hta_docs.txt")    


# if __name__ == "__main__":
#     run_query("tell me what biomarker is used in which country and agency", ['21860'])