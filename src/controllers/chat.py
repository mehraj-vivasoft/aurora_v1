from fastapi import APIRouter
# from langchain.llms import OpenAI
# from langchain.chains import LLMChain
# from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from pydantic import BaseModel
from src.services.azure.azure_openai import run_query

# Load environment variables
load_dotenv()

router = APIRouter()

# # Initialize OpenAI LLM
# llm = OpenAI(temperature=0.7)

# # Create a prompt template
# prompt = PromptTemplate(
#     input_variables=["topic"],
#     template="Write a brief summary about {topic}."
# )

# # Create LLM chain
# chain = LLMChain(llm=llm, prompt=prompt)


class ChatRequest(BaseModel):
    query: str
    filtered_ids: list[str] = []

@router.post("/")
async def generate_text(chat_request: ChatRequest) -> str:
    try:
        # Generate response using LangChain    
        res = run_query(chat_request.query, chat_request.filtered_ids)
        return res
    except Exception as e:
        return {"error": str(e)}
