from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from langchain_community.utilities import SQLDatabase
import pandas as pd

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

def get_list_from_query(query: str) -> list[str]:
    _, engine = get_db()
    
    # Read directly using pandas
    df = pd.read_sql_query(query, engine)
    
    # If the query returns a single column, return it as a list
    if len(df.columns) == 1:
        return df[df.columns[0]].tolist()
    
    # If multiple columns, return the dataframe
    return df