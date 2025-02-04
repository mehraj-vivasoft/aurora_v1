import pandas as pd
from src.services.database.get_db import get_db
from src.services.load.model import HTARecord, HTARecords


def convert_df_to_pydantic(df: pd.DataFrame) -> HTARecords:
    records = []
    for _, row in df.iterrows():
        # Convert row to dict and handle any NaN values
        row_dict = row.where(pd.notna(row), None).to_dict()
        # Convert column names to snake_case
        row_dict = {k.lower(): v for k, v in row_dict.items()}
        records.append(HTARecord(**row_dict))
    return HTARecords(records=records)


def get_hta_records(query: str) -> HTARecords:
    db, engine = get_db()
    df = pd.read_sql_query(query, engine)
    hta_records = convert_df_to_pydantic(df)
    return hta_records