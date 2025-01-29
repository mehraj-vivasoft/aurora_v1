from scripts.rag_summary import HTARecord


def get_header(hta_entry: HTARecord) -> str:
    
    return f"""
    Here is the HTA(Health Technology Assessment) metrics for the drug {hta_entry.drug_name} conducted in {hta_entry.country} by {hta_entry.hta_agency_name} in {hta_entry.hta_decision_dt}.
    It's for the treatment of  {hta_entry.primary_disease}, with the following details - 
        biomarkers : {hta_entry.biomarkers},
        drug combination : {hta_entry.drug_combinations},
        treatment modality : {hta_entry.treatment_modality},
        rwe(real-world evidence) : {hta_entry.rwe_used},
        hta status : {hta_entry.hta_status} 
    """