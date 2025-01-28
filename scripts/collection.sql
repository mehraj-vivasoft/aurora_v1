-- all countries
SELECT Distinct(COUNTRY) from dbo.HTA; 
SELECT Distinct(HTA_AGENCY_NAME) from dbo.HTA; 
SELECT Distinct(DRUG_NAME) from dbo.HTA; 
SELECT Distinct(BIOMARKERS) from dbo.HTA; 
SELECT Distinct(TREATMENT_MODALITY) from dbo.HTA; 
SELECT Distinct(PRIMARY_DISEASE) from dbo.HTA;
SELECT Distinct(FINAL_RECOMMENDATION) from dbo.HTA;
SELECT
    *
FROM
    dbo.HTA
WHERE
    HTA_DECISION_DT between '2020' and '2024'
or
    HTA_DECISION_DT >= '2024';
