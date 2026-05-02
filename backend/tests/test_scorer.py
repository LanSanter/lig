from backend.services.draft_generator import generate_result


def test_generation_score_range():
    result = generate_result("測試")
    assert 0 <= result.score <= 1
