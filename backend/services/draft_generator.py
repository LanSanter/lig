import json

from backend.schemas.generation_result import GenerationResult, TriggerCandidate
from backend.services.llm_client import default_model, generate_with_openai, load_prompt
from backend.services.sample_loader import load_oneshot_samples


def _fallback_result(user_input: str) -> GenerationResult:
    trigger = TriggerCandidate(
        source="關鍵詞",
        misheard_as="近音詞",
        explanation="由輸入文字中抽取近音或語意錯位",
        score=0.75,
    )
    warnings: list[str] = []
    if "歌詞" in user_input:
        warnings.append("本內容包含版權歌詞風險，請謹慎分享")
    return GenerationResult(
        text=f"{trigger.misheard_as}漸漸光，{user_input[:30]}在此刻突然變成群體合唱。",
        score=0.8,
        trigger_used=trigger,
        safety_passed=True,
        warnings=warnings,
    )


def generate_result(user_input: str) -> GenerationResult:
    system_prompt = load_prompt("draft_generator")
    one_shot = load_oneshot_samples().get("samples", [])
    user_prompt = json.dumps(
        {
            "user_input": user_input,
            "one_shot_samples": one_shot,
            "output_schema": {
                "text": "str",
                "score": "float",
                "trigger_used": {"source": "str", "misheard_as": "str", "explanation": "str", "score": "float"},
                "safety_passed": "bool",
                "warnings": ["str"],
            },
        },
        ensure_ascii=False,
    )
    raw = generate_with_openai(
        provider="openai",
        model=default_model("openai"),
        system_prompt=system_prompt,
        user_prompt=user_prompt,
    )
    try:
        parsed = json.loads(raw)
        return GenerationResult(**parsed)
    except Exception:
        return _fallback_result(user_input)
