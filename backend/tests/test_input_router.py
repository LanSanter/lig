from backend.services.input_router import route_input


def test_route_input_short_text_returns_options():
    result = route_input("今天很累")
    assert result["mode"] == "ask_user_to_choose"
    assert len(result["options"]) >= 2
