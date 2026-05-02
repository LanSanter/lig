from pydantic import BaseModel, Field


class TriggerCandidate(BaseModel):
    source: str
    misheard_as: str
    explanation: str
    score: float


class GenerationResult(BaseModel):
    text: str
    score: float
    trigger_used: TriggerCandidate
    safety_passed: bool
    warnings: list[str] = Field(default_factory=list)
