import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from src.rag_pipeline import run_rag

app = FastAPI()

cors_origins = os.getenv("CORS_ORIGINS", "")
origins = [origin.strip() for origin in cors_origins.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    domain: str = "consumer"   # default domain


@app.post("/chat")
async def chat(req: ChatRequest):
    try:
        response = run_rag(req.message, req.domain)
        return {"response": response}

    except Exception as e:
        return {"response": f"Error: {str(e)}"}