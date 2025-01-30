from fastapi import FastAPI
from src.controllers import health, filters, chat
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Project Aurora",
    description="Backend for Project Aurora",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(filters.router, prefix="/filters", tags=["Filters"])
app.include_router(chat.router, prefix="/chat", tags=["Chat"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
