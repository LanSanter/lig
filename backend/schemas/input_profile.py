from pydantic import BaseModel, Field


class InputProfile(BaseModel):
    raw_text: str
    location: str | None = None
    characters: list[str] = Field(default_factory=list)
    event: str | None = None
    key_terms: list[str] = Field(default_factory=list)
    tone: list[str] = Field(default_factory=list)
    style: list[str] = Field(default_factory=list)
    trigger_candidates: list[str] = Field(default_factory=list)
    sufficiency_score: float = 0.0
    missing_slots: list[str] = Field(default_factory=list)
