from fastapi import APIRouter
from src.services.database.execute import get_list_from_query

router = APIRouter()


@router.get("/countries")
async def get_available_countries():
    try:
        results = get_list_from_query("SELECT Distinct(COUNTRY) from dbo.HTA")
        print("raw results", results)
        return {"countries": results}
    except Exception as e:
        return {"error": str(e)}

@router.get("/agencies")
async def get_available_agencies():
    try:
        results = get_list_from_query("SELECT Distinct(HTA_AGENCY_NAME) from dbo.HTA")
        print("raw results", results)
        return {"agencies": results}
    except Exception as e:
        return {"error": str(e)}
    
@router.get("/drugs")
async def get_available_drugs():
    try:
        results = get_list_from_query("SELECT Distinct(DRUG_NAME) from dbo.HTA")
        print("raw results", results)
        return {"drugs": results}
    except Exception as e:
        return {"error": str(e)}
    
@router.get("/biomarkers")
async def get_available_biomarkers():
    try:
        results = get_list_from_query("SELECT Distinct(BIOMARKERS) from dbo.HTA")
        print("raw results", results)
        return {"biomarkers": results}
    except Exception as e:
        return {"error": str(e)}
    
@router.get("/modalities")
async def get_available_modalities():
    try:
        results = get_list_from_query("SELECT Distinct(TREATMENT_MODALITY) from dbo.HTA")
        print("raw results", results)
        return {"modalities": results}
    except Exception as e:
        return {"error": str(e)}
    
@router.get("/diseases")
async def get_available_diseases():
    try:
        results = get_list_from_query("SELECT Distinct(PRIMARY_DISEASE) from dbo.HTA")
        print("raw results", results)
        return {"diseases": results}
    except Exception as e:
        return {"error": str(e)}

@router.get("/final_recommendations")
async def get_available_final_reccomandations():
    try:
        results = get_list_from_query("SELECT Distinct(FINAL_RECOMMENDATION) from dbo.HTA")
        print("raw results", results)
        return {"final_recommendations": results}
    except Exception as e:
        return {"error": str(e)}