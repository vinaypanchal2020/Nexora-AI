import json
from fastapi import APIRouter, Form, File, UploadFile
from typing import Optional
from app.rag.pipeline import general_chat, rag_chat

router = APIRouter()

@router.post("/")
def home():
    return {"message": "Welcome to AI Chatbot"}

@router.post("/chat")
async def chat(
    message: str = Form(...),
    history: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None)
):
    parsed_history = []
    if history:
        try:
            parsed_history = json.loads(history)
        except json.JSONDecodeError:
            parsed_history = []

    if file:
        return await rag_chat(
            message=message,
            file=file,
            history=parsed_history
        )
    else:
        return await general_chat(
            message=message,
            history=parsed_history
        )