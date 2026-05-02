from backend.schemas.input_profile import InputProfile
from backend.services.scenario_expander import scenario_expander


def compute_sufficiency(profile: InputProfile) -> float:
    score = 0.0
    if profile.location:
        score += 0.20
    if profile.characters:
        score += 0.20
    if profile.event:
        score += 0.25
    if profile.key_terms or profile.trigger_candidates:
        score += 0.25
    if profile.tone or profile.style:
        score += 0.10
    return score


def extract_profile(raw_text: str) -> InputProfile:
    profile = InputProfile(raw_text=raw_text)
    if "在" in raw_text:
        profile.location = "未明地點"
    if len(raw_text) >= 20:
        profile.event = raw_text[:40]
    if "店員" in raw_text:
        profile.characters.append("店員")
    if "Tensor" in raw_text or "天色" in raw_text:
        profile.trigger_candidates.append("Tensor/天色")
    profile.missing_slots = [
        slot for slot, value in {
            "location": profile.location,
            "characters": profile.characters,
            "event": profile.event,
            "trigger_candidates": profile.trigger_candidates,
        }.items()
        if not value
    ]
    profile.sufficiency_score = compute_sufficiency(profile)
    return profile


def route_input(raw_text: str) -> dict:
    profile = extract_profile(raw_text)
    if profile.sufficiency_score >= 0.65:
        return {"mode": "direct_generate", "profile": profile}
    return {
        "mode": "ask_user_to_choose",
        "profile": profile,
        "options": scenario_expander(profile),
    }
