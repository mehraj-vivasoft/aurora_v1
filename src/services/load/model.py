from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class HTARecord(BaseModel):
    id: Optional[str] = None
    hta_agency_name: Optional[str] = None
    country: Optional[str] = None
    hta_decision_dt: Optional[str] = None
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
    evendence_synthesis: Optional[str] = None 
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