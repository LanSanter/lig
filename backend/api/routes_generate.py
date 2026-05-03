from fastapi import APIRouter
from pydantic import BaseModel

from backend.services.draft_generator import generate_result
from backend.schemas.generation_result import GenerateRequest, GenerationResult

router = APIRouter(tags=["generate"])



@router.post("/generate", response_model=GenerationResult)
def generate(req: GenerateRequest) -> GenerationResult:
    result = generate_result(req)
    print(f"生成結果: {result}")
    return result
