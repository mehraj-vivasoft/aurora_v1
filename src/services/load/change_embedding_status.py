from src.services.load.status import LoadStatus
from src.services.load.queries.chng_embding_status import get_query_of_change_embedding_status_by_filename
from src.services.load.queries.chng_embedding_status_by_id import get_query_of_change_embedding_status_by_filename_and_id
from src.services.load.get_hta_records import get_hta_records
from src.services.load.model import HTARecords
from src.services.database.get_db import get_db


def execute_query(query: str):
    db, engine = get_db()
    db.run(query)
    
        
def change_embedding_status(file_name: str, from_status: LoadStatus, to_status: LoadStatus):
    
    query = get_query_of_change_embedding_status_by_filename(file_name, from_status, to_status)
    
    return execute_query(query)

def change_embedding_status_by_id(file_name: str, from_status: LoadStatus, to_status: LoadStatus, id: str):
    
    query = get_query_of_change_embedding_status_by_filename_and_id(file_name, from_status, to_status, id)
    
    return execute_query(query)