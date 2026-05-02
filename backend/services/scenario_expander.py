from backend.schemas.input_profile import InputProfile
from backend.schemas.scenario_option import ScenarioOption
from backend.services.sample_loader import load_oneshot_samples


def scenario_expander(profile: InputProfile) -> list[ScenarioOption]:
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

    if not options:
        options.append(
            ScenarioOption(
                id="A",
                title="便利商店覺醒",
                scene=f"{base}，大夜班掃條碼後全店開始合唱。",
                characters=["店員", "顧客"],
                trigger_candidates=["barcode/八口"],
                escalation_hint="貨架商品開始自發排隊",
                tone=["日常", "感動"],
            )
        )

    return options
