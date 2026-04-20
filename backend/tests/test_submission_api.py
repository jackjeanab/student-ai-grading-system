from fastapi.testclient import TestClient

from app.api import submissions
from app.main import app


def test_rejects_invalid_xml_before_evaluation() -> None:
    client = TestClient(app)

    response = client.post(
        "/api/submissions",
        json={
            "assignment_id": 101,
            "activity_id": 1,
            "xml_content": "<xml><broken>",
        },
        headers={"Authorization": "Bearer student-token"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid XML format"


def test_orchestrates_parser_rules_ai_and_final_decision(monkeypatch) -> None:
    calls: list[tuple] = []

    def fake_parse_blockly_xml(xml_content: str) -> dict[str, list[str]]:
        calls.append(("parser", xml_content))
        return {"root_block_types": ["board_initializes_setup"], "all_block_types": ["board_initializes_setup"]}

    def fake_evaluate_rules(parsed: dict, rules: dict) -> dict:
        calls.append(("rule_engine", parsed, rules))
        return {"rule_status": "pass", "missing_blocks": [], "final_light": None, "final_grade": None}

    class FakeLLMService:
        def __init__(self, model_name: str = "", transport=None) -> None:
            calls.append(("llm_init", model_name))

        def evaluate(self, parsed: dict, assignment_prompt: str) -> dict:
            calls.append(("ai", parsed, assignment_prompt))
            return {"light": "yellow", "grade": "pending"}

    def fake_decide_final_result(rule_result: dict, ai_result: dict) -> dict:
        calls.append(("decide", rule_result, ai_result))
        return {"light": "yellow", "grade": "pending", "source": "ai"}

    monkeypatch.setattr(submissions, "parse_blockly_xml", fake_parse_blockly_xml)
    monkeypatch.setattr(submissions, "evaluate_rules", fake_evaluate_rules)
    monkeypatch.setattr(submissions, "LLMService", FakeLLMService)
    monkeypatch.setattr(submissions, "decide_final_result", fake_decide_final_result)

    result = submissions._orchestrate_submission_evaluation("<xml />")

    assert result["final_result"]["source"] == "ai"
    assert [step[0] for step in calls] == ["parser", "rule_engine", "llm_init", "ai", "decide"]
