from fastapi import APIRouter
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

router = APIRouter()

# Initialize OpenAI LLM
llm = OpenAI(temperature=0.7)

# Create a prompt template
prompt = PromptTemplate(
    input_variables=["topic"],
    template="Write a brief summary about {topic}."
)

# Create LLM chain
chain = LLMChain(llm=llm, prompt=prompt)


@router.get("/generate/{topic}")
async def generate_text(topic: str):
    try:
        # Generate response using LangChain
        response = chain.run(topic=topic)
        return {"topic": topic, "response": response}
    except Exception as e:
        return {"error": str(e)}
