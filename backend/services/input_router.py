import json
from backend.schemas.input_profile import InputProfile
from backend.services.scenario_expander import scenario_expander
from backend.services.llm_client import generate_with_openai, load_prompt



def extract_profile(raw_text: str) -> InputProfile:
    # 1. 呼叫 AI 進行情境解析
    system_prompt = load_prompt("scene_analyzer")
    raw_response = generate_with_openai(
        model="gpt-4.1-mini",
        system_prompt=system_prompt,
        user_prompt=f"使用者輸入：{raw_text}"
    )
    
    try:
        data = json.loads(raw_response)
        # 將 AI 抽取的結果轉為 InputProfile 物件
        profile = InputProfile(raw_text=raw_text, **data)
    except Exception:
        # Fallback 機制：至少維持 raw_text
        profile = InputProfile(raw_text=raw_text)

    # 2. 判斷缺失欄位與計算分數 (邏輯維持計畫書定義)
    profile.missing_slots = [
        slot for slot, value in {
            "location": profile.location,
            "characters": profile.characters,
            "event": profile.event,
            "trigger_candidates": profile.trigger_candidates,
        }.items() if not value
    ]
    return profile



def route_input(raw_text: str) -> dict:
    profile = extract_profile(raw_text)
    options = scenario_expander(profile)
    return {
        "mode": "ask_user_to_choose",
        "profile": profile,
        "options": options,
    }
