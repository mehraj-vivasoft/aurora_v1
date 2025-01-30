from langchain_core.documents import Document
from typing import List

from scripts.final.model import HTARecord
from scripts.templates.header import get_header
from scripts.templates.metadata import get_metadata
from scripts.templates.domain_kb import get_domain_intro

domains = [
    "general_hta_conclusion",
    "intervention_add_details",
    "comparator_add_details",
    "data_packages",
    "outcomes_from_evidence",
    "coa_details",
    "econ_model_design",
    "payer_decision",
    "rwe_details",
    "clinical_outcomes"
]

def get_large_docs(hta_entry: HTARecord) -> List[Document]:
    
    header = get_header(hta_entry)
    docs = []
    
    for domain in domains:
        
        raw_page = _get_raw_page(domain, hta_entry) 
        print("domain : ", domain)               
        
        content = f"""{header}
        The content below {get_domain_intro(domain)}
        
        # Content:
        {raw_page}
        """
        
        docs.append(
            Document(
                page_content=content,
                metadata=get_metadata(hta_entry)
            )
        )
    
    return docs

def _get_raw_page(domain: str, hta_entry: HTARecord) -> str:
    if domain == "general_hta_conclusion":
        raw_page = hta_entry.general_hta_conclusion
    elif domain == "intervention_add_details":
        raw_page = hta_entry.intervention_add_details
    elif domain == "comparator_add_details":
        raw_page = hta_entry.comparator_add_details
    elif domain == "data_packages":
        raw_page = hta_entry.data_packages
    elif domain == "outcomes_from_evidence":
        raw_page = hta_entry.outcomes_from_evidence
    elif domain == "coa_details":
        raw_page = hta_entry.coa_details
    elif domain == "econ_model_design":
        raw_page = hta_entry.econ_model_design
    elif domain == "payer_decision":
        raw_page = hta_entry.payer_decision
    elif domain == "rwe_details":
        raw_page = hta_entry.rwe_details
    elif domain == "clinical_outcomes":
        raw_page = hta_entry.clinical_outcomes
    else:
        raw_page = ""
    
    return raw_page