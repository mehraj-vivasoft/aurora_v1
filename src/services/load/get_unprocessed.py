from src.services.load.status import LoadStatus
from src.services.load.queries.query_by_filename import get_query_by_filename
from src.services.load.get_hta_records import get_hta_records
from src.services.load.model import HTARecords


def get_unprocessed_docs(file_name: str) -> HTARecords:
    
    query = get_query_by_filename(file_name, LoadStatus.UNPROCESSED)
    
    return get_hta_records(query)