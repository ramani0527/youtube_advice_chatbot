from fastapi import APIRouter
from pydantic import BaseModel
from src.utils.retriever import TranscriptRetriever
from src.utils.generator import generate_answer

router = APIRouter()
retriever = TranscriptRetriever()

class AskRequest(BaseModel):
    question: str
    top_k: int = 5

@router.post("/ask")
def ask(req: AskRequest):
    retrieved = retriever.search(req.question, top_k=req.top_k )
    answer = generate_answer(req.question, retrieved)
    return {"question": req.question, "answer": answer, "chunks": retrieved}
