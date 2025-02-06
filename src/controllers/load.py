from fastapi import APIRouter, BackgroundTasks
from dotenv import load_dotenv
from pydantic import BaseModel
from src.services.load.load_unprocessed import load_unprocessed_data_in_background

# Load environment variables
load_dotenv()

router = APIRouter()

class LoadUnprocessedRequest(BaseModel):
    file_name: str
    index_name: str = "processed-index-v2-test"

@router.post("/unprocessed")
async def load_unprocessed(load_unprocessed_request: LoadUnprocessedRequest, background_tasks: BackgroundTasks):
    try:
        await load_unprocessed_data_in_background(load_unprocessed_request.file_name, load_unprocessed_request.index_name, background_tasks)
        return f"Started loading unprocessed data from {load_unprocessed_request.file_name}"
    except Exception as e:
        return {"error": str(e)}

@router.get("/unprocessed")
async def get_unprocessed():
    try:
        
        return "get unprocessed"
    except Exception as e:
        return {"error": str(e)}

@router.get("/pending")
async def get_pending():
    try:
        
        return "get pending"
    except Exception as e:
        return {"error": str(e)}
    
@router.post("/pending")
async def load_pending():
    try:
        
        return "Start loading pending data"
    except Exception as e:
        return {"error": str(e)}
