from backend.schemas.input_profile import InputProfile
from backend.services.scenario_expander import scenario_expander


GENERIC_TONE_HINTS = ["感動", "荒謬", "熱血", "厭世", "溫柔"]


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
    text = raw_text.strip()
    profile = InputProfile(raw_text=text)

    words = [w for w in text.replace("，", " ").replace(",", " ").split() if w]
    profile.key_terms = words[:6]

    for tone in GENERIC_TONE_HINTS:
        if tone in text:
            profile.tone.append(tone)

    if len(words) >= 2:
        profile.event = " ".join(words[: min(10, len(words))])

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
    options = scenario_expander(profile)
    return {
        "mode": "ask_user_to_choose",
        "profile": profile,
        "options": options,
    }
