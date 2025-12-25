from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from controllers.mcp_controller import process_user_query

router = APIRouter()

class ChatRequest(BaseModel):
    question: str

@router.post("/chat")
async def chat(request: ChatRequest):
    try:
        answer = await process_user_query(request.question)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))