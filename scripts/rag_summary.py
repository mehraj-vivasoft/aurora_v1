from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
import pandas as pd

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class HTARecord(BaseModel):
    id: Optional[int] = None
    hta_agency_name: Optional[str] = None
    country: Optional[str] = None
    hta_decision_dt: Optional[datetime] = None
    biomarkers: Optional[str] = None
    primary_disease: Optional[str] = None
    drug_name: Optional[str] = None
    generic_drug_name: Optional[str] = None
    drug_combinations: Optional[str] = None
    general_hta_conclusion: Optional[str] = None
    dosing: Optional[str] = None
    treatment_duration: Optional[str] = None
    intervention_add_details: Optional[str] = None
    treatment_line: Optional[str] = None
    treatment_modality: Optional[str] = None
    comparator_drugs: Optional[str] = None
    comparator_combination_therapy: Optional[str] = None
    comparator_drugs_payers: Optional[str] = None
    comparator_add_details: Optional[str] = None
    target_population: Optional[str] = None
    asmr_requested: Optional[str] = None
    asmr_recieved: Optional[str] = None
    clinical_outcomes: Optional[str] = None
    data_packages: Optional[str] = None
    study_type: Optional[str] = None
    evendence_synthesis: Optional[str] = None  # Note: keeping the typo as it's in the original data
    outcomes_from_evidence: Optional[str] = None
    coa_instruments: Optional[str] = None
    coa_type: Optional[str] = None
    coa_details: Optional[str] = None
    rwe_used: Optional[str] = None
    rwe_data_type: Optional[str] = None
    rwe_payer_accepted: Optional[str] = None
    hta_analysis_type: Optional[str] = None
    cea_effectiveness_measure: Optional[str] = None
    econ_model: Optional[str] = None
    time_horizon: Optional[str] = None
    econ_model_design: Optional[str] = None
    payer_decision: Optional[str] = None
    key_drive_ce: Optional[str] = None
    clinical_positives: Optional[str] = None
    clinical_negatives: Optional[str] = None
    final_recommendation: Optional[str] = None
    subgroup_name: Optional[str] = None
    hta_status: Optional[str] = None
    quintiles_link: Optional[str] = None
    web_url: Optional[str] = None
    reimbursed_indication: Optional[str] = None
    rwe_details: Optional[str] = None


class HTARecords(BaseModel):
    records: List[HTARecord]


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
SELECT TOP 5 
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

# Instead of using SQLDatabase.run(), use the engine directly with pandas
df = pd.read_sql_query(query, engine)


# Convert DataFrame to list of Pydantic models
def convert_df_to_pydantic(df):
    records = []
    for _, row in df.iterrows():
        # Convert row to dict and handle any NaN values
        row_dict = row.where(pd.notna(row), None).to_dict()
        # Convert column names to snake_case
        row_dict = {k.lower(): v for k, v in row_dict.items()}
        records.append(HTARecord(**row_dict))
    return HTARecords(records=records)


# Convert your DataFrame to Pydantic models
hta_records = convert_df_to_pydantic(df)

print(hta_records.records[0].drug_name)

print(hta_records.records[0].country)

print(hta_records.records[0].hta_decision_dt)

print(hta_records.records[0].primary_disease)

print(hta_records.records[0].clinical_outcomes)

print(len(hta_records.records))
