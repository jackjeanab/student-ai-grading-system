from __future__ import annotations

import json
from collections.abc import Callable
from dataclasses import dataclass

from app.core.config import settings
from app.services.evaluation_service import mock_ai_evaluate

DEFAULT_GEMINI_MODEL = "gemini-2.5-flash-lite"

EvaluateFn = Callable[[dict, str, str], dict]
ClientFactory = Callable[[str], object]

ALLOWED_LIGHTS = {"green", "blue", "yellow", "red"}
DEFAULT_GRADES = {
    "green": "優",
    "blue": "良",
    "yellow": "可",
    "red": "需改進",
}


@dataclass(slots=True)
class LLMService:
    model_name: str = settings.gemini_model or DEFAULT_GEMINI_MODEL
    api_key: str = settings.gemini_api_key
    transport: EvaluateFn | None = None
    client_factory: ClientFactory | None = None

    def build_prompt(self, parsed: dict, assignment_prompt: str) -> str:
        block_types = ", ".join(parsed.get("all_block_types", [])) or "none"
        root_block_types = ", ".join(parsed.get("root_block_types", [])) or "none"
        return "\n".join(
            [
                "You are grading a student's Arduino Blockly XML submission.",
                "Return JSON only with exactly these keys: light, grade, feedback.",
                "Allowed light values: green, blue, yellow, red.",
                "Use green for excellent, blue for good, yellow for partially complete, red for serious issues.",
                f"Assignment prompt: {assignment_prompt or '(missing)'}",
                f"Root block types: {root_block_types}",
                f"All detected block types: {block_types}",
            ]
        )

    def evaluate(self, parsed: dict, assignment_prompt: str) -> dict:
        if self.transport is None:
            if not self.api_key:
                return mock_ai_evaluate(parsed, assignment_prompt)

            try:
                return self._evaluate_with_gemini(parsed, assignment_prompt)
            except Exception:
                return self._fallback_result()

        return self.transport(parsed, assignment_prompt, self.model_name)

    def _evaluate_with_gemini(self, parsed: dict, assignment_prompt: str) -> dict:
        client = self._create_client()
        response = client.models.generate_content(
            model=self.model_name,
            contents=self.build_prompt(parsed, assignment_prompt),
        )
        return self._normalize_response(self._extract_text(response))

    def _create_client(self) -> object:
        if self.client_factory is not None:
            return self.client_factory(self.api_key)

        from google import genai

        return genai.Client(api_key=self.api_key)

    def _extract_text(self, response: object) -> str:
        text = getattr(response, "text", "")
        if isinstance(text, str) and text.strip():
            return text

        raise ValueError("Gemini response did not include text.")

    def _normalize_response(self, response_text: str) -> dict:
        payload = json.loads(self._strip_code_fence(response_text))
        light = str(payload.get("light", "")).lower().strip()
        if light not in ALLOWED_LIGHTS:
            raise ValueError(f"Unsupported light value: {light}")

        feedback = str(payload.get("feedback", "")).strip()
        return {
            "light": light,
            "grade": str(payload.get("grade") or DEFAULT_GRADES[light]),
            "feedback": feedback or "AI grading completed.",
            "source": "gemini",
        }

    def _strip_code_fence(self, response_text: str) -> str:
        text = response_text.strip()
        if text.startswith("```"):
            lines = text.splitlines()
            if lines and lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].startswith("```"):
                lines = lines[:-1]
            text = "\n".join(lines).strip()
        return text

    def _fallback_result(self) -> dict:
        return {
            "light": "yellow",
            "grade": DEFAULT_GRADES["yellow"],
            "feedback": "AI grading is temporarily unavailable; please review this submission manually.",
            "source": "fallback",
        }
