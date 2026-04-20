from fastapi import APIRouter, Header, HTTPException, status

from app.schemas.submission import SubmissionCreate
from app.services import decide_final_result, evaluate_rules, parse_blockly_xml
from app.services.llm_service import LLMService
from app.services.xml_validator import validate_blockly_xml

router = APIRouter(prefix="/api/submissions", tags=["submissions"])


def _orchestrate_submission_evaluation(
    xml_content: str,
    assignment_prompt: str = "",
    rules: dict[str, object] | None = None,
) -> dict[str, object]:
    parsed = parse_blockly_xml(xml_content)
    rule_result = evaluate_rules(parsed, rules or {})
    ai_result = LLMService().evaluate(parsed, assignment_prompt)
    final_result = decide_final_result(rule_result, ai_result)

    return {
        "parsed": parsed,
        "rule_result": rule_result,
        "ai_result": ai_result,
        "final_result": final_result,
    }


@router.post("", status_code=status.HTTP_202_ACCEPTED)
def create_submission(
    payload: SubmissionCreate,
    authorization: str | None = Header(default=None),
) -> dict[str, str]:
    if authorization != "Bearer student-token":
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        validate_blockly_xml(payload.xml_content)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    _orchestrate_submission_evaluation(payload.xml_content)
    return {"status": "queued"}
