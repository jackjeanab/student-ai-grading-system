from app.services.evaluation_service import decide_final_result


def test_rule_engine_overrides_ai_when_conflicting() -> None:
    rule_result = {
        "final_light": "red",
        "final_grade": "待加強",
        "rule_status": "hard_fail",
        "feedback": "Missing required blocks: delay_custom",
    }
    ai_result = {"light": "green", "grade": "優", "feedback": "Looks complete."}

    result = decide_final_result(rule_result, ai_result)

    assert result["light"] == "red"
    assert result["grade"] == "待加強"
    assert result["source"] == "rule_engine"
    assert result["feedback"] == "Missing required blocks: delay_custom"


def test_ai_feedback_is_preserved_when_rules_pass() -> None:
    rule_result = {
        "final_light": None,
        "final_grade": None,
        "rule_status": "pass",
        "feedback": "",
    }
    ai_result = {
        "light": "blue",
        "grade": "良",
        "feedback": "Uses setup and loop, but timing could be clearer.",
    }

    result = decide_final_result(rule_result, ai_result)

    assert result["light"] == "blue"
    assert result["grade"] == "良"
    assert result["feedback"] == "Uses setup and loop, but timing could be clearer."
    assert result["source"] == "ai"
