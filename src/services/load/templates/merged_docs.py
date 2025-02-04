from langchain_core.documents import Document
from typing import List

from src.services.load.model import HTARecord
from src.services.load.templates.header import get_header
from src.services.load.templates.metadata import get_metadata

merged_intros = [
    "Here is the details about the treatment and its alternatives, including dosage, drug combinations, duration, treatment line, modality, payer-approved comparator drugs and combination therapy",
    "The data below focuses on target population, coa (clinical outcome analysis) and clinical results, including treatment benefits, risks, and subgroup-specific responses.",
    "Following data includes study types, real-world evidence (RWE) types, evidence synthesis and payer-accepted data sources for decision-making.",
    "Following data covers health technology assessment (HTA) and economic modeling aspects, including cost-effectiveness measures, key drivers, reimbursed indication and time horizons."
]

def get_merged_docs(hta_entry: HTARecord) -> List[Document]:
    
    header = get_header(hta_entry)
    docs = []
    
    for idx, intro in enumerate(merged_intros):
        
        raw_page = _get_raw_page(intro, hta_entry, idx)        
        
        content = f"""{header}
                        
        {raw_page}
        """
        
        docs.append(
            Document(
                page_content=content,
                entry_id=hta_entry.id,
                metadata=get_metadata(hta_entry)
            )
        )
    
    return docs

def _get_raw_page(intro: str, hta_entry: HTARecord, indx: int) -> str:
    
    raw_page = f"""{intro}
    
    #Content:
    { _get_content(indx, hta_entry) }
    """
    
    return raw_page

def _get_content(indx: int, hta_entry: HTARecord) -> str:
    
    content = ""
    
    if indx == 0:
        content = f"""Dosing: {hta_entry.dosing}
        drug combination: {hta_entry.drug_combinations}
        treatment duration: {hta_entry.treatment_duration}
        treatment line: {hta_entry.treatment_line}
        treatment modality: {hta_entry.treatment_modality}
        comparator drugs: {hta_entry.comparator_drugs}
        comparator combination threapy: {hta_entry.comparator_combination_therapy}
        comparator drugs payers: {hta_entry.comparator_drugs_payers}
        """
    
    elif indx == 1:
        content = f"""target population: {hta_entry.target_population}
        subgroup name: {hta_entry.subgroup_name}
        clinical positives: {hta_entry.clinical_positives}
        clinical negatives: {hta_entry.clinical_negatives}
        coa instruments: {hta_entry.coa_instruments}
        coa types: {hta_entry.coa_type}
        """
        
    elif indx == 2:
        content = f"""study types: {hta_entry.study_type}
        evidence synthesis: {hta_entry.evendence_synthesis}
        rwe data type: {hta_entry.rwe_data_type}
        rwe payer accepted: {hta_entry.rwe_payer_accepted}
        """
        
    elif indx == 3:
        content = f"""hta analysis type: {hta_entry.hta_analysis_type}
        cea effectiveness measure: {hta_entry.cea_effectiveness_measure}
        econ model: {hta_entry.econ_model}
        time horizon: {hta_entry.time_horizon}
        key drive ce: {hta_entry.key_drive_ce}
        reimbursed indication: {hta_entry.reimbursed_indication}
        """
    
    return content