from fastapi import APIRouter
from pydantic import BaseModel

from backend.services.input_router import route_input

router = APIRouter(tags=["scenario"])


class ScenarioRequest(BaseModel):
    user_input: str


@router.post("/scenario")
def scenario(req: ScenarioRequest) -> dict:
    return route_input(req.user_input)
