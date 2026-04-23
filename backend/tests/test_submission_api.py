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


def test_create_submission_saves_evaluation_without_exposing_api_key(monkeypatch) -> None:
    client = TestClient(app)
    calls: list[tuple] = []

    class FakeSession:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, traceback) -> None:
            return None

    def fake_get_assignment_prompt(session, assignment_id: int) -> str:
        calls.append(("prompt", assignment_id))
        return "Teacher configured prompt"

    def fake_orchestrate(xml_content: str, assignment_prompt: str, rules=None) -> dict[str, object]:
        calls.append(("orchestrate", xml_content, assignment_prompt, rules))
        return {
            "final_result": {
                "light": "blue",
                "grade": "良",
                "feedback": "Good first pass.",
                "source": "gemini",
            }
        }

    def fake_save_submission_evaluation(session, payload, evaluation_payload, student_id: int) -> dict[str, object]:
        calls.append(("save", payload.assignment_id, evaluation_payload["final_result"], student_id))
        return {
            "submission_id": 55,
            "activity_id": payload.activity_id,
            "assignment_id": payload.assignment_id,
            "light": "blue",
            "grade": "良",
            "feedback": "Good first pass.",
            "source": "gemini",
        }

    monkeypatch.setattr(submissions, "get_assignment_prompt", fake_get_assignment_prompt)
    monkeypatch.setattr(submissions, "_orchestrate_submission_evaluation", fake_orchestrate)
    monkeypatch.setattr(submissions, "save_submission_evaluation", fake_save_submission_evaluation)
    monkeypatch.setattr(submissions, "get_session_local", lambda: FakeSession)

    response = client.post(
        "/api/submissions",
        json={
            "assignment_id": 101,
            "activity_id": 1,
            "xml_content": '<xml xmlns="https://developers.google.com/blockly/xml" />',
        },
        headers={"Authorization": "Bearer student-token"},
    )

    body = response.json()
    assert response.status_code == 202
    assert body["status"] == "evaluated"
    assert body["submission_id"] == 55
    assert body["feedback"] == "Good first pass."
    assert "api_key" not in body
    assert "GEMINI_API_KEY" not in str(body)
    assert [call[0] for call in calls] == ["prompt", "orchestrate", "save"]


def test_create_submission_uses_prompt_sent_with_student_answer(monkeypatch) -> None:
    client = TestClient(app)
    calls: list[tuple] = []

    class FakeSession:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, traceback) -> None:
            return None

    def fake_get_assignment_prompt(session, assignment_id: int) -> str:
        calls.append(("prompt", assignment_id))
        return "Database prompt should not be used"

    def fake_orchestrate(xml_content: str, assignment_prompt: str, rules=None) -> dict[str, object]:
        calls.append(("orchestrate", assignment_prompt))
        return {
            "final_result": {
                "light": "blue",
                "grade": "良",
                "feedback": "同學有依照題目完成基本控制。",
                "source": "gemini",
            }
        }

    def fake_save_submission_evaluation(session, payload, evaluation_payload, student_id: int) -> dict[str, object]:
        calls.append(("save", payload.assignment_prompt))
        return {
            "submission_id": 56,
            "activity_id": payload.activity_id,
            "assignment_id": payload.assignment_id,
            "light": "blue",
            "grade": "良",
            "feedback": "同學有依照題目完成基本控制。",
            "source": "gemini",
        }

    monkeypatch.setattr(submissions, "get_assignment_prompt", fake_get_assignment_prompt)
    monkeypatch.setattr(submissions, "_orchestrate_submission_evaluation", fake_orchestrate)
    monkeypatch.setattr(submissions, "save_submission_evaluation", fake_save_submission_evaluation)
    monkeypatch.setattr(submissions, "get_session_local", lambda: FakeSession)

    response = client.post(
        "/api/submissions",
        json={
            "assignment_id": 101,
            "activity_id": 1,
            "assignment_prompt": "請設計 LED 每 1 秒閃爍一次。",
            "xml_content": '<xml xmlns="https://developers.google.com/blockly/xml" />',
        },
        headers={"Authorization": "Bearer student-token"},
    )

    assert response.status_code == 202
    assert ("prompt", 101) not in calls
    assert ("orchestrate", "請設計 LED 每 1 秒閃爍一次。") in calls
    assert ("save", "請設計 LED 每 1 秒閃爍一次。") in calls
