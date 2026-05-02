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
    system_prompt = load_prompt("scenario_expander")
    one_shot = load_oneshot_samples().get("samples", [])
    user_prompt = json.dumps(
        {
            "user_input": profile.raw_text,
            "missing_slots": profile.missing_slots,
            "one_shot_samples": one_shot,
            "instruction": "請輸出 ScenarioOption JSON array",
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
        return [ScenarioOption(**item) for item in parsed]
    except Exception:
        return _fallback_options(profile)
