from backend.services.draft_generator import generate_result


def test_generation_default_safety_passed():
    result = generate_result("測試")
    assert result.safety_passed is True
