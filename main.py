from fastapi import FastAPI, Request, Depends, HTTPException
from src.controllers import health, filters, chat, load
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

HARD_CODED_PASSWORD = "WblmUPGOJLSJY1B/q3Sd95KqxMdvUz4sWj6SYWw/JqE"

def verify_auth(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    token = auth_header.split(" ")[1]
    if token != HARD_CODED_PASSWORD:
        raise HTTPException(status_code=403, detail="Forbidden")

app.include_router(health.router)
app.include_router(filters.router, prefix="/filters", tags=["Filters"])
app.include_router(chat.router, prefix="/chat", tags=["Chat"], dependencies=[Depends(verify_auth)])
app.include_router(load.router, prefix="/load", tags=["Load Data"], dependencies=[Depends(verify_auth)])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
