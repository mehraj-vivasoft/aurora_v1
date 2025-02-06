from src.services.load.status import LoadStatus


def get_query_of_change_embedding_status_by_filename_and_id(file_name: str, from_status: LoadStatus, to_status: LoadStatus, id: str) -> str:
    query = f"""
    UPDATE dbo.temp_HTA_Data
    SET EMBEDDING_STATUS = '{to_status}'
    WHERE FILE_NAME = '{file_name}' AND EMBEDDING_STATUS = '{from_status} AND ID = {id}'
    """
    return query