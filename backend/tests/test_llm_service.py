from app.services.llm_service import LLMService


def test_evaluate_without_api_key_uses_local_fallback() -> None:
    parsed = {"all_block_types": ["a", "b", "c", "d", "e", "f", "g", "h"]}

    result = LLMService(api_key="").evaluate(parsed, "Make the LED blink.")

    assert result["light"] == "green"
    assert result["source"] == "mock"
    assert result["feedback"]
    assert "同學" in result["feedback"]


def test_build_prompt_requires_json_and_includes_assignment_context() -> None:
    prompt = LLMService(api_key="test-key").build_prompt(
        {"all_block_types": ["board_initializes_setup", "delay_custom"]},
        "Use Arduino blocks to blink an LED.",
    )

    assert "Return JSON only" in prompt
    assert "green, blue, yellow, red" in prompt
    assert "Use Arduino blocks to blink an LED." in prompt
    assert "board_initializes_setup" in prompt


def test_build_prompt_requires_taiwan_traditional_chinese_teacher_voice() -> None:
    prompt = LLMService(api_key="test-key").build_prompt(
        {"all_block_types": ["board_initializes_setup", "delay_custom"]},
        "讓 LED 閃爍。",
    )

    assert "台灣繁體中文" in prompt
    assert "國中資訊老師" in prompt
    assert "鼓勵" in prompt


def test_evaluate_with_gemini_client_parses_json_response() -> None:
    calls: dict[str, str] = {}

    class FakeResponse:
        text = '{"light":"blue","grade":"good","feedback":"Uses setup and delay blocks."}'

    class FakeModels:
        def generate_content(self, *, model: str, contents: str) -> FakeResponse:
            calls["model"] = model
            calls["contents"] = contents
            return FakeResponse()

    class FakeClient:
        models = FakeModels()

    result = LLMService(
        api_key="test-key",
        model_name="gemini-test",
        client_factory=lambda api_key: FakeClient(),
    ).evaluate({"all_block_types": ["board_initializes_setup"]}, "Blink an LED.")

    assert calls["model"] == "gemini-test"
    assert "Blink an LED." in calls["contents"]
    assert result == {
        "light": "blue",
        "grade": "good",
        "feedback": "Uses setup and delay blocks.",
        "source": "gemini",
    }


def test_evaluate_falls_back_to_yellow_when_gemini_fails() -> None:
    class BrokenModels:
        def generate_content(self, *, model: str, contents: str) -> object:
            raise RuntimeError("network unavailable")

    class BrokenClient:
        models = BrokenModels()

    result = LLMService(
        api_key="test-key",
        client_factory=lambda api_key: BrokenClient(),
    ).evaluate({"all_block_types": []}, "Blink an LED.")

    assert result["light"] == "yellow"
    assert result["source"] == "fallback"
    assert "老師" in result["feedback"]
    assert "稍後" in result["feedback"]
