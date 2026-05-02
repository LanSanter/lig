from backend.schemas.input_profile import InputProfile
from backend.schemas.scenario_option import ScenarioOption


def scenario_expander(profile: InputProfile) -> list[ScenarioOption]:
    base = profile.raw_text or "日常場景"
    return [
        ScenarioOption(
            id="A",
            title="科技實驗室驚魂",
            scene=f"{base}，工程師在 debug 時突然群體合唱。",
            characters=["工程師", "實習生"],
            trigger_candidates=["Tensor/天色", "Kernel/可樂"],
            escalation_hint="螢幕訊號變成演唱會燈光",
            tone=["爆肝", "荒謬"],
        ),
        ScenarioOption(
            id="B",
            title="便利商店覺醒",
            scene="大夜班掃條碼後，音效觸發全店同步和聲。",
            characters=["店員", "顧客"],
            trigger_candidates=["Barcode/八口", "latte/拿鐵"],
            escalation_hint="貨架商品開始自發排隊",
            tone=["日常", "感動"],
        ),
    ]
