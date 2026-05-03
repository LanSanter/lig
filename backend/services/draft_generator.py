import json

from backend.schemas.generation_result import GenerateRequest, GenerationResult, TriggerCandidate
from backend.services.llm_client import default_model, generate_with_openai, load_prompt
from backend.services.sample_loader import load_oneshot_samples


def _fallback_result(req: GenerateRequest) -> GenerationResult:
    trigger = TriggerCandidate(
        source="關鍵詞",
        misheard_as="近音詞",
        explanation="由輸入文字中抽取近音或語意錯位",
        score=0.75,
    )
    warnings: list[str] = []
    if "歌詞" in req.user_input:
        warnings.append("本內容包含版權歌詞風險，請謹慎分享")
    return GenerationResult(
        text=f"{trigger.misheard_as}漸漸光，{req.user_input[:30]}在此刻突然變成群體合唱。",
        score=0.8,
        trigger_used=trigger,
        safety_passed=True,
        warnings=warnings,
    )


def generate_result(req: GenerateRequest) -> GenerationResult:
    system_prompt = load_prompt("draft_generator")
    one_shot = load_oneshot_samples().get("samples", [])
    
    # 建立一個更詳細的上下文給 AI
    context = {
        "user_input": req.user_input,
        "constraints": {
            "characters": req.characters,
            "selected_trigger": req.trigger,
            "desired_tone": req.tone
        },
        "one_shot_samples": one_shot,
        "instruction": "請根據 user_input 與 constraints 中的角色、觸發梗進行生成。輸出格式須嚴格遵守 JSON。",
        "output_schema": {
            "text": "str",
            "score": "float",
            "trigger_used": {
                "source": "str", 
                "misheard_as": "str", 
                "explanation": "str", 
                "score": "float"
            },
            "safety_passed": "bool",
            "warnings": ["str"],
        },
    }

    raw = generate_with_openai(
        model=default_model("openai"),
        system_prompt=system_prompt,
        user_prompt=json.dumps(context, ensure_ascii=False),
    )

    try:
        # 清理可能存在的 Markdown 代碼塊標籤
        cleaned_json = raw.replace("```json", "").replace("```", "").strip()
        parsed = json.loads(cleaned_json)
        return GenerationResult(**parsed)
    except Exception as e:
        print(f"解析失敗: {e}, 原始內容: {raw}")
        return _fallback_result(req)
