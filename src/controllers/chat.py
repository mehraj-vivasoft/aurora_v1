from typing import Union
from fastapi import APIRouter
from dotenv import load_dotenv
from pydantic import BaseModel
from src.services.azure.azure_openai import run_query, run_stream
from fastapi.responses import StreamingResponse

# Load environment variables
load_dotenv()

router = APIRouter()

class ChatRequest(BaseModel):
    query: str
    filtered_ids: list[str] = []
    prev_messages: list[str] = []

@router.post("/")
async def chat_response(chat_request: ChatRequest):
    try:                
        res = run_query(chat_request.query, chat_request.filtered_ids, chat_request.prev_messages)
        return res
    except Exception as e:
        return "error" + str(e)
    
@router.post("/stream")
async def chat_stream(chat_request: ChatRequest):
    try:
        return StreamingResponse(
            run_stream(chat_request.query, chat_request.filtered_ids, chat_request.prev_messages), 
            media_type="text/plain"
        )
    except Exception as e:
        return "error" + str(e)
