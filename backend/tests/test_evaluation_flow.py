from app.services.evaluation_service import decide_final_result


def test_rule_engine_overrides_ai_when_conflicting() -> None:
    rule_result = {
        "final_light": "red",
        "final_grade": "待加強",
        "rule_status": "hard_fail",
    }
    ai_result = {"light": "green", "grade": "優"}

    result = decide_final_result(rule_result, ai_result)

    assert result["light"] == "red"
    assert result["grade"] == "待加強"
    assert result["source"] == "rule_engine"
