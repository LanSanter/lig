from pydantic import BaseModel, Field


class ScenarioOption(BaseModel):
    id: str
    title: str
    scene: str
    characters: list[str] = Field(default_factory=list)
    trigger_candidates: list[str] = Field(default_factory=list)
    escalation_hint: str
    tone: list[str] = Field(default_factory=list)
