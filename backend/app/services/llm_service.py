from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from app.services.evaluation_service import mock_ai_evaluate

DEFAULT_GEMINI_MODEL = "gemini-2.5-flash-lite"

EvaluateFn = Callable[[dict, str, str], dict]


@dataclass(slots=True)
class LLMService:
    model_name: str = DEFAULT_GEMINI_MODEL
    transport: EvaluateFn | None = None

    def build_prompt(self, parsed: dict, assignment_prompt: str) -> str:
        block_types = ", ".join(parsed.get("all_block_types", [])) or "none"
        return "\n".join(
            [
                f"Model: {self.model_name}",
                f"Assignment prompt: {assignment_prompt or '(missing)'}",
                f"Detected blocks: {block_types}",
            ]
        )

    def evaluate(self, parsed: dict, assignment_prompt: str) -> dict:
        if self.transport is None:
            return mock_ai_evaluate(parsed, assignment_prompt)

        return self.transport(parsed, assignment_prompt, self.model_name)
