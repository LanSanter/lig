import json

from backend.schemas.input_profile import InputProfile
from backend.schemas.scenario_option import ScenarioOption
from backend.services.llm_client import default_model, generate_with_openai, load_prompt
from backend.services.sample_loader import load_oneshot_samples


def _fallback_options(profile: InputProfile) -> list[ScenarioOption]:
    dataset = load_oneshot_samples().get("samples", [])
    base = profile.raw_text.strip() or "日常場景"
    options: list[ScenarioOption] = []
    for idx, sample in enumerate(dataset[:3], start=1):
        trigger = sample.get("trigger", {})
        scene = sample.get("scene", {})
        tones = sample.get("output_style", {}).get("tone", ["荒謬"])
        options.append(
            ScenarioOption(
                id=chr(64 + idx),
                title=f"{scene.get('location', '城市角落')}共鳴事件",
                scene=f"{base}。延伸為：{scene.get('event', '突發日常事件')}。",
                characters=scene.get("characters", []),
                trigger_candidates=[f"{trigger.get('source', '詞')}/{trigger.get('misheard_as', '空耳')}"],
                escalation_hint="現場群體被一個近音詞觸發並同步進入合唱敘事",
                tone=tones,
            )
        )
    return options


def scenario_expander(profile: InputProfile) -> list[ScenarioOption]:
    # 第一步：使用 Trigger Miner 挖掘關鍵點
    trigger_miner_prompt = load_prompt("trigger_miner")
    miner_input = {
        "scene": profile.event or profile.raw_text,
        "key_terms": profile.key_terms
    }
    
    raw_triggers = generate_with_openai(
        model="gpt-4.1-mini",
        system_prompt=trigger_miner_prompt,
        user_prompt=json.dumps(miner_input, ensure_ascii=False)
    )
    
    # 第二步：將挖掘到的梗餵給 Scenario Expander 擴展選項
    expander_system_prompt = load_prompt("scenario_expander")
    user_context = {
        "user_input": profile.raw_text,
        "extracted_triggers": raw_triggers, # 讓 AI 根據這些梗來設計場景
        "missing_slots": profile.missing_slots,
        "instruction": "請參考 extracted_triggers 中的諧音梗，設計 3-5 個荒謬且熱血的情境選項。輸出 JSON array。"
    }

    raw_scenarios = generate_with_openai(
        model="gpt-4.1-mini",
        system_prompt=expander_system_prompt,
        user_prompt=json.dumps(user_context, ensure_ascii=False)
    )

    try:
        parsed = json.loads(raw_scenarios)
        print("Parsed scenarios:", parsed)  # Debug log
        return [ScenarioOption(**item) for item in parsed]
    except Exception as e:
        print("Error message:", e)
        return _fallback_options(profile)
