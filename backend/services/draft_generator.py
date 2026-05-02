from backend.schemas.generation_result import GenerationResult, TriggerCandidate


def generate_result(user_input: str) -> GenerationResult:
    return GenerationResult(
        text=(
            "天色漸漸光，收銀機的嗶聲像合唱指揮棒，"
            "整間店的人對著展示機唱起希望。"
        ),
        score=0.95,
        trigger_used=TriggerCandidate(
            source="Tensor",
            misheard_as="天色",
            explanation="英文近音觸發台式敘事轉折",
            score=0.92,
        ),
        safety_passed=True,
        warnings=[],
    )
