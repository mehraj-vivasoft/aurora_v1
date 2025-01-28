from fastapi import FastAPI
from controllers import query, health
import uvicorn

app = FastAPI(
    title="Project Aurora",
    description="Backend for Project Aurora",
    version="1.0.0"
)

app.include_router(health.router)
app.include_router(query.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
