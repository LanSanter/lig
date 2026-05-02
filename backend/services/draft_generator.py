from backend.schemas.generation_result import GenerationResult, TriggerCandidate
from backend.services.sample_loader import load_oneshot_samples


def _select_trigger(user_input: str) -> TriggerCandidate:
    samples = load_oneshot_samples().get("samples", [])
    for sample in samples:
        token = sample.get("trigger", {}).get("source", "")
        if token and token.lower() in user_input.lower():
            t = sample["trigger"]
            return TriggerCandidate(
                source=t["source"],
                misheard_as=t["misheard_as"],
                explanation=t["explanation"],
                score=0.9,
            )

    return TriggerCandidate(
        source="關鍵詞",
        misheard_as="近音詞",
        explanation="由輸入文字中抽取近音或語意錯位",
        score=0.75,
    )


def generate_result(user_input: str) -> GenerationResult:
    trigger = _select_trigger(user_input)
    preview = user_input[:30] + ("..." if len(user_input) > 30 else "")

    generated = (
        f"{trigger.misheard_as}漸漸光，{preview}在此刻突然變成群體合唱，"
        "每個人都把日常誤聽成希望，最後在島嶼夜色裡收束成一段溫柔。"
    )

    warnings: list[str] = []
    if "歌詞" in user_input:
        warnings.append("本內容包含版權歌詞風險，請謹慎分享")

    return GenerationResult(
        text=generated,
        score=0.88 if trigger.score >= 0.9 else 0.8,
        trigger_used=trigger,
        safety_passed=True,
        warnings=warnings,
    )
