from collections.abc import Generator

from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_session_local
from app.schemas.submission import SubmissionCreate
from app.services import (
    decide_final_result,
    evaluate_rules,
    get_assignment_prompt,
    get_submission_evaluation,
    parse_blockly_xml,
    save_submission_evaluation,
)
from app.services.llm_service import LLMService
from app.services.xml_validator import validate_blockly_xml

router = APIRouter(prefix="/api/submissions", tags=["submissions"])
STUDENT_ID_PLACEHOLDER = 1


def get_db_session() -> Generator[Session]:
    session = get_session_local()()
    try:
        yield session
    finally:
        session.close()


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
) -> dict[str, object]:
    if authorization != "Bearer student-token":
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        validate_blockly_xml(payload.xml_content)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    with get_session_local()() as session:
        assignment_prompt = (payload.assignment_prompt or "").strip() or get_assignment_prompt(
            session,
            payload.assignment_id,
        )
        evaluation_payload = _orchestrate_submission_evaluation(
            payload.xml_content,
            assignment_prompt,
        )
        saved = save_submission_evaluation(
            session,
            payload,
            evaluation_payload,
            student_id=STUDENT_ID_PLACEHOLDER,
        )
    return {"status": "evaluated", **saved}


@router.get("/{submission_id}/evaluation")
def read_submission_evaluation(
    submission_id: int,
    authorization: str | None = Header(default=None),
    session: Session = Depends(get_db_session),
) -> dict[str, object]:
    if authorization not in {"Bearer student-token", "Bearer dev-token"}:
        raise HTTPException(status_code=401, detail="Unauthorized")

    result = get_submission_evaluation(session, submission_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Submission evaluation not found")

    return result
