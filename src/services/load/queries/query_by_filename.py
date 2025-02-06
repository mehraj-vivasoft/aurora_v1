from src.services.load.status import LoadStatus


def get_query_by_filename(file_name: str, embedding_status: LoadStatus) -> str:
    query = f"""
    SELECT 
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
    FROM dbo.temp_HTA_Data
    WHERE FILE_NAME = '{file_name}' AND
    EMBEDDING_STATUS = '{embedding_status}'
    """
    return query