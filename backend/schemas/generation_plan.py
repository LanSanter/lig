from pydantic import BaseModel, Field


class GenerationPlan(BaseModel):
    setup: str
    trigger: str
    glitch_start: str
    collective_spread: str
    escalation: list[str] = Field(default_factory=list)
    emotional_turn: str
    ideological_closure: str
