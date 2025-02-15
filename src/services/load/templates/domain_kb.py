from pydantic import BaseModel

class DomainKnowledge(BaseModel):
    general_hta_conclusion: str
    intervention_add_details: str
    comparator_add_details: str
    data_packages: str
    outcomes_from_evidence: str
    coa_details: str
    econ_model_design: str
    payer_decision: str
    rwe_details: str
    clinical_outcomes: str

domain_knowledge = DomainKnowledge(
    general_hta_conclusion= "Summarizes the overall findings and conclusions from a health technology assessment (HTA), focusing on the effectiveness, safety, and cost-efficiency of the intervention.",
    intervention_add_details= "Provides additional information about the specific intervention being evaluated, including its intended use, characteristics and mechanisms.",
    comparator_add_details= "Contains supplementary details about the comparator used in the evaluation, such as alternative treatments or standard care practices.",
    data_packages= "Refers to the datasets or documentation submitted for the assessment, including clinical trial results, observational studies, and other supporting evidence.",
    outcomes_from_evidence= "Highlights key outcomes derived from evidence, such as efficacy, safety profiles, or other measurable impacts of the intervention or comparator.",
    coa_details= "Includes details about Clinical Outcome Assessments (COA), such as instruments or measures used to evaluate patient-reported or clinical outcomes.",
    econ_model_design= "Describes the design and structure of the economic model used to assess the cost-effectiveness or budget impact of the intervention.",
    payer_decision= "Captures the decisions or recommendations made by payers or reimbursement agencies based on the assessment findings.",
    rwe_details= "Provides insights from Real-World Evidence (RWE), such as data from observational studies, registries, or real-world clinical practice to supplement trial findings.",
    clinical_outcomes= "Captures key results from clinical studies, including the effectiveness and safety of an intervention. It typically includes measures such as survival rates, disease progression, symptom improvement, and adverse effects."
)

def get_domain_intro(domain: str) -> str:
    if domain == "general_hta_conclusion":
        return domain_knowledge.general_hta_conclusion
    elif domain == "intervention_add_details":
        return domain_knowledge.intervention_add_details
    elif domain == "comparator_add_details":
        return domain_knowledge.comparator_add_details
    elif domain == "data_packages":
        return domain_knowledge.data_packages
    elif domain == "outcomes_from_evidence":
        return domain_knowledge.outcomes_from_evidence
    elif domain == "coa_details":
        return domain_knowledge.coa_details
    elif domain == "econ_model_design":
        return domain_knowledge.econ_model_design
    elif domain == "payer_decision":
        return domain_knowledge.payer_decision
    elif domain == "rwe_details":
        return domain_knowledge.rwe_details
    elif domain == "clinical_outcomes":
        return domain_knowledge.clinical_outcomes
    else:
        return ""
