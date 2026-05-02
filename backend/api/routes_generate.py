from fastapi import APIRouter
from pydantic import BaseModel

from backend.services.draft_generator import generate_result

router = APIRouter(tags=["generate"])


class GenerateRequest(BaseModel):
    user_input: str
    

@router.post("/generate")
def generate(req: GenerateRequest) -> dict:
    result = generate_result(req.user_input)
    return result.model_dump()
