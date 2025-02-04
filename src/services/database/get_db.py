from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from langchain_community.utilities import SQLDatabase

def get_db():
    load_dotenv()

    connection_string = (
        f"mssql+pyodbc://{os.getenv('SQL_USERNAME')}:{os.getenv('SQL_PASSWORD')}@"
        f"{os.getenv('SQL_SERVER')}/"
        f"{os.getenv('SQL_DATABASE')}?driver={os.getenv('ODBCDRIVER')}"
    )

    engine = create_engine(connection_string)
    db = SQLDatabase(engine=engine)

    return db, engine