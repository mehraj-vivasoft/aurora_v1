from fastapi import FastAPI
from src.controllers import health, filters
import uvicorn

app = FastAPI(
    title="Project Aurora",
    description="Backend for Project Aurora",
    version="1.0.0"
)

app.include_router(health.router)
app.include_router(filters.router, prefix="/filters", tags=["Filters"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
