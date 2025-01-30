from typing import Dict
from scripts.rag_summary import HTARecord


def get_metadata(hta_entry: HTARecord) -> Dict[str, str]:
    
    return {
        "entry_id": hta_entry.id,
        "drug_name": hta_entry.drug_name,
        "country": hta_entry.country,
        "hta_agency_name": hta_entry.hta_agency_name,
        "hta_decision_dt": hta_entry.hta_decision_dt,
        "primary_disease": hta_entry.primary_disease,
        "biomarkers": hta_entry.biomarkers,
        "drug_combinations": hta_entry.drug_combinations,
        "treatment_modality": hta_entry.treatment_modality,
        "rwe_used": hta_entry.rwe_used,
        "hta_status": hta_entry.hta_status                    
    }        