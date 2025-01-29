from fastapi import APIRouter, Query
from typing import List, Optional
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
async def get_available_final_recommendations():
    try:
        results = get_list_from_query("SELECT Distinct(FINAL_RECOMMENDATION) from dbo.HTA")
        print("raw results", results)
        return {"final_recommendations": results}
    except Exception as e:
        return {"error": str(e)}
    
@router.get("/get_ids")
async def get_filtered_ids(
    countries: Optional[List[str]] = Query(None),
    agencies: Optional[List[str]] = Query(None),
    drugs: Optional[List[str]] = Query(None),
    biomarkers: Optional[List[str]] = Query(None),
    modalities: Optional[List[str]] = Query(None),
    diseases: Optional[List[str]] = Query(None),
    final_recommendations: Optional[List[str]] = Query(None)
):
    try:
        filters = []
        
        filter_mappings = {
            'COUNTRY': countries,
            'HTA_AGENCY_NAME': agencies,
            'DRUG_NAME': drugs,
            'BIOMARKERS': biomarkers,
            'TREATMENT_MODALITY': modalities,
            'PRIMARY_DISEASE': diseases,
            'FINAL_RECOMMENDATION': final_recommendations
        }
        
        for column, values in filter_mappings.items():
            if values:
                formatted_values = [f"'{value}'" for value in values]
                filters.append(f"{column} IN ({', '.join(formatted_values)})")
        
        query = "SELECT ID FROM dbo.HTA"
        if filters:
            query += " WHERE " + " AND ".join(filters)
            
        print("Generated query:", query)
        results = get_list_from_query(query)
        return {"ids": results}
    except Exception as e:
        return {"error": str(e)}