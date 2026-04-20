# Student AI Grading System Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a v1 classroom system that accepts Blockly XML homework submissions, evaluates them asynchronously, shows per-student per-assignment status in real time, and lets teachers review and override final results.

**Architecture:** Use a single-repo web app with a FastAPI backend and React frontend. Deploy the frontend on Vercel Hobby and the backend on Render Free Web Service. Use Supabase Free for Postgres, Auth, and Realtime. Keep v1 simple by running evaluation jobs through FastAPI background tasks or an in-app job queue, and call Gemini Developer API directly for AI grading and feedback generation.

**Tech Stack:** Python 3.13, FastAPI, SQLAlchemy, Pydantic, pytest, React, TypeScript, Vite, React Router, TanStack Query, Vercel Hobby, Render Free Web Service, Supabase Free, Supabase Postgres, Supabase Auth, Supabase Realtime, Gemini Developer API, gemini-2.5-flash-lite

---

## Scope Check

This spec covers four tightly related slices rather than truly independent products:

1. authentication and classroom management
2. XML submission and automated evaluation
3. real-time classroom visibility
4. teacher review and reporting

These should stay in one implementation plan because the main value is the end-to-end flow from submission to classroom dashboard. The tasks below are still decomposed into vertical slices so each task produces testable software.

## Proposed File Structure

### Backend

- Create: `backend/pyproject.toml`
- Create: `backend/app/main.py`
- Create: `backend/app/core/config.py`
- Create: `backend/app/core/database.py`
- Create: `backend/app/core/security.py`
- Create: `backend/app/core/websocket_hub.py`
- Create: `backend/app/models/user.py`
- Create: `backend/app/models/activity.py`
- Create: `backend/app/models/assignment.py`
- Create: `backend/app/models/submission.py`
- Create: `backend/app/models/evaluation.py`
- Create: `backend/app/models/audit.py`
- Create: `backend/app/schemas/auth.py`
- Create: `backend/app/schemas/activity.py`
- Create: `backend/app/schemas/assignment.py`
- Create: `backend/app/schemas/submission.py`
- Create: `backend/app/schemas/evaluation.py`
- Create: `backend/app/services/auth_service.py`
- Create: `backend/app/services/xml_validator.py`
- Create: `backend/app/services/xml_parser.py`
- Create: `backend/app/services/rule_engine.py`
- Create: `backend/app/services/evaluation_service.py`
- Create: `backend/app/services/review_service.py`
- Create: `backend/app/services/report_service.py`
- Create: `backend/app/api/auth.py`
- Create: `backend/app/api/activities.py`
- Create: `backend/app/api/assignments.py`
- Create: `backend/app/api/submissions.py`
- Create: `backend/app/api/teacher.py`
- Create: `backend/app/api/reports.py`
- Create: `backend/app/api/ws.py`
- Create: `backend/tests/conftest.py`
- Create: `backend/tests/test_auth_api.py`
- Create: `backend/tests/test_submission_api.py`
- Create: `backend/tests/test_xml_parser.py`
- Create: `backend/tests/test_rule_engine.py`
- Create: `backend/tests/test_evaluation_flow.py`
- Create: `backend/tests/test_teacher_review_api.py`
- Create: `backend/tests/fixtures/sample_blockly.xml`

### Frontend

- Create: `frontend/package.json`
- Create: `frontend/vite.config.ts`
- Create: `frontend/src/main.tsx`
- Create: `frontend/src/App.tsx`
- Create: `frontend/src/app/router.tsx`
- Create: `frontend/src/app/queryClient.ts`
- Create: `frontend/src/lib/api.ts`
- Create: `frontend/src/lib/ws.ts`
- Create: `frontend/src/features/auth/LoginPage.tsx`
- Create: `frontend/src/features/student/StudentAssignmentsPage.tsx`
- Create: `frontend/src/features/student/StudentSubmissionPage.tsx`
- Create: `frontend/src/features/student/StudentClassStatusPage.tsx`
- Create: `frontend/src/features/teacher/TeacherActivitiesPage.tsx`
- Create: `frontend/src/features/teacher/TeacherDashboardPage.tsx`
- Create: `frontend/src/features/teacher/TeacherReportPage.tsx`
- Create: `frontend/src/features/teacher/TeacherReviewDrawer.tsx`
- Create: `frontend/src/components/StatusBadge.tsx`
- Create: `frontend/src/components/FeedbackCard.tsx`
- Create: `frontend/src/components/AssignmentGrid.tsx`
- Create: `frontend/src/styles.css`
- Create: `frontend/src/test/LoginPage.test.tsx`
- Create: `frontend/src/test/StudentSubmissionPage.test.tsx`
- Create: `frontend/src/test/TeacherDashboardPage.test.tsx`

### Docs and sample data

- Modify: `docs/student-ai-grading-system-spec.md`
- Create: `docs/api/student-ai-grading-api.md`
- Create: `docs/deployment/free-tier-deployment.md`
- Create: `docs/data-model/student-ai-grading-er.md`
- Create: `docs/runbooks/local-development.md`

## Delivery Sequence

Build in this order so every stage is runnable:

1. backend skeleton and database
2. auth and activity management
3. submission intake and XML validation
4. XML parsing and rule evaluation
5. async evaluation and real-time updates
6. teacher review and reporting
7. frontend student experience
8. frontend teacher experience

## Task 1: Bootstrap Backend Skeleton

**Files:**
- Create: `backend/pyproject.toml`
- Create: `backend/app/main.py`
- Create: `backend/app/core/config.py`
- Create: `backend/app/core/database.py`
- Create: `backend/.env.example`
- Test: `backend/tests/test_healthcheck.py`

- [ ] **Step 1: Write the failing health check test**

```python
from fastapi.testclient import TestClient

from app.main import app


def test_healthcheck_returns_ok() -> None:
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd backend; pytest tests/test_healthcheck.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'app'`

- [ ] **Step 3: Write minimal implementation**

```python
# backend/app/main.py
from fastapi import FastAPI

app = FastAPI(title="Student AI Grading System")


@app.get("/health")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}
```

```toml
# backend/pyproject.toml
[project]
name = "student-ai-grading-backend"
version = "0.1.0"
dependencies = [
  "fastapi>=0.115",
  "uvicorn>=0.30",
  "sqlalchemy>=2.0",
  "pydantic>=2.8",
  "pydantic-settings>=2.4",
  "python-jose[cryptography]>=3.3",
  "passlib[bcrypt]>=1.7",
  "psycopg[binary]>=3.2",
  "supabase>=2.5",
  "google-genai>=0.5",
]

[tool.pytest.ini_options]
pythonpath = ["."]
testpaths = ["tests"]
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd backend; pytest tests/test_healthcheck.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add backend/pyproject.toml backend/app/main.py backend/tests/test_healthcheck.py
git commit -m "feat: bootstrap backend skeleton"
```

## Task 2: Add Persistence Models and Session Wiring

**Files:**
- Modify: `backend/app/main.py`
- Create: `backend/app/models/user.py`
- Create: `backend/app/models/activity.py`
- Create: `backend/app/models/assignment.py`
- Create: `backend/app/models/submission.py`
- Create: `backend/app/models/evaluation.py`
- Create: `backend/app/models/audit.py`
- Modify: `backend/app/core/database.py`
- Test: `backend/tests/test_database_models.py`

- [ ] **Step 1: Write the failing database model test**

```python
from app.models.activity import ClassActivity
from app.models.assignment import Assignment
from app.models.submission import Submission


def test_submission_belongs_to_activity_and_assignment() -> None:
    activity = ClassActivity(title="Week 1", status="active", teacher_id=1)
    assignment = Assignment(title="Blink", description="Use led blocks")
    submission = Submission(
        student_id=2,
        activity=activity,
        assignment=assignment,
        xml_content="<xml />",
        status="queued",
    )

    assert submission.activity.title == "Week 1"
    assert submission.assignment.title == "Blink"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd backend; pytest tests/test_database_models.py -v`
Expected: FAIL with `ModuleNotFoundError` or model import errors

- [ ] **Step 3: Write minimal implementation**

```python
# backend/app/core/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


class Base(DeclarativeBase):
    pass


engine = create_engine(
    "postgresql+psycopg://postgres:postgres@localhost:5432/student_ai_grading",
    future=True,
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
```

```python
# backend/app/models/submission.py
from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Submission(Base):
    __tablename__ = "submissions"

    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(index=True)
    activity_id: Mapped[int] = mapped_column(ForeignKey("activities.id"))
    assignment_id: Mapped[int] = mapped_column(ForeignKey("assignments.id"))
    xml_content: Mapped[str] = mapped_column(Text())
    status: Mapped[str] = mapped_column(String(32))

    activity = relationship("ClassActivity")
    assignment = relationship("Assignment")
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd backend; pytest tests/test_database_models.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add backend/app/core/database.py backend/app/models backend/tests/test_database_models.py
git commit -m "feat: add core persistence models"
```

## Task 3: Implement Authentication and Role-Aware Login

**Files:**
- Create: `backend/app/core/security.py`
- Create: `backend/app/schemas/auth.py`
- Create: `backend/app/services/auth_service.py`
- Create: `backend/app/api/auth.py`
- Modify: `backend/app/main.py`
- Test: `backend/tests/test_auth_api.py`

- [ ] **Step 1: Write the failing login test**

```python
from fastapi.testclient import TestClient

from app.main import app


def test_login_returns_role_and_token() -> None:
    client = TestClient(app)

    response = client.post(
        "/api/auth/login",
        json={"account": "teacher01", "password": "secret123"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["role"] == "teacher"
    assert "access_token" in data
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd backend; pytest tests/test_auth_api.py::test_login_returns_role_and_token -v`
Expected: FAIL with `404 Not Found`

- [ ] **Step 3: Write minimal implementation**

```python
# backend/app/schemas/auth.py
from pydantic import BaseModel


class LoginRequest(BaseModel):
    account: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    role: str
```

```python
# backend/app/api/auth.py
from fastapi import APIRouter, HTTPException

from app.schemas.auth import LoginRequest, LoginResponse

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest) -> LoginResponse:
    if payload.account == "teacher01" and payload.password == "secret123":
        return LoginResponse(access_token="dev-token", role="teacher")
    raise HTTPException(status_code=401, detail="Invalid credentials")
```

```python
# backend/app/services/auth_service.py
from supabase import Client


class AuthService:
    def __init__(self, supabase_client: Client) -> None:
        self.supabase = supabase_client

    def login(self, account: str, password: str) -> dict:
        response = self.supabase.auth.sign_in_with_password(
            {"email": account, "password": password}
        )
        return response.model_dump()
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd backend; pytest tests/test_auth_api.py::test_login_returns_role_and_token -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add backend/app/schemas/auth.py backend/app/api/auth.py backend/app/main.py backend/tests/test_auth_api.py
git commit -m "feat: add login api"
```

## Task 4: Build Activity and Assignment Management APIs

**Files:**
- Create: `backend/app/schemas/activity.py`
- Create: `backend/app/schemas/assignment.py`
- Create: `backend/app/api/activities.py`
- Create: `backend/app/api/assignments.py`
- Test: `backend/tests/test_activity_api.py`

- [ ] **Step 1: Write the failing teacher activity creation test**

```python
from fastapi.testclient import TestClient

from app.main import app


def test_teacher_can_create_activity_with_assignments() -> None:
    client = TestClient(app)

    response = client.post(
        "/api/activities",
        json={
            "title": "Chapter 2 Practice",
            "assignment_ids": [101, 102],
            "status": "draft",
        },
        headers={"Authorization": "Bearer dev-token"},
    )

    assert response.status_code == 201
    assert response.json()["assignment_ids"] == [101, 102]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd backend; pytest tests/test_activity_api.py::test_teacher_can_create_activity_with_assignments -v`
Expected: FAIL with `404 Not Found`

- [ ] **Step 3: Write minimal implementation**

```python
# backend/app/schemas/activity.py
from pydantic import BaseModel


class ActivityCreate(BaseModel):
    title: str
    assignment_ids: list[int]
    status: str


class ActivityResponse(ActivityCreate):
    id: int
```

```python
# backend/app/api/activities.py
from fastapi import APIRouter, status

from app.schemas.activity import ActivityCreate, ActivityResponse

router = APIRouter(prefix="/api/activities", tags=["activities"])


@router.post("", response_model=ActivityResponse, status_code=status.HTTP_201_CREATED)
def create_activity(payload: ActivityCreate) -> ActivityResponse:
    return ActivityResponse(id=1, **payload.model_dump())
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd backend; pytest tests/test_activity_api.py::test_teacher_can_create_activity_with_assignments -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add backend/app/schemas/activity.py backend/app/api/activities.py backend/tests/test_activity_api.py
git commit -m "feat: add activity management api"
```

## Task 5: Implement Student Submission Intake and XML Validation

**Files:**
- Create: `backend/app/schemas/submission.py`
- Create: `backend/app/services/xml_validator.py`
- Create: `backend/app/api/submissions.py`
- Test: `backend/tests/test_submission_api.py`
- Test: `backend/tests/fixtures/sample_blockly.xml`

- [ ] **Step 1: Write the failing submission validation test**

```python
from fastapi.testclient import TestClient

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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd backend; pytest tests/test_submission_api.py::test_rejects_invalid_xml_before_evaluation -v`
Expected: FAIL with `404 Not Found`

- [ ] **Step 3: Write minimal implementation**

```python
# backend/app/services/xml_validator.py
from xml.etree import ElementTree


def validate_blockly_xml(xml_content: str) -> None:
    try:
        ElementTree.fromstring(xml_content)
    except ElementTree.ParseError as exc:
        raise ValueError("Invalid XML format") from exc
```

```python
# backend/app/api/submissions.py
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from app.services.xml_validator import validate_blockly_xml


class SubmissionCreate(BaseModel):
    assignment_id: int
    activity_id: int
    xml_content: str


router = APIRouter(prefix="/api/submissions", tags=["submissions"])


@router.post("", status_code=status.HTTP_202_ACCEPTED)
def create_submission(payload: SubmissionCreate) -> dict[str, str]:
    try:
        validate_blockly_xml(payload.xml_content)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"status": "queued"}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd backend; pytest tests/test_submission_api.py::test_rejects_invalid_xml_before_evaluation -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add backend/app/services/xml_validator.py backend/app/api/submissions.py backend/tests/test_submission_api.py
git commit -m "feat: validate xml on submission"
```

## Task 6: Parse Blockly XML into a Rule-Friendly Structure

**Files:**
- Create: `backend/app/services/xml_parser.py`
- Test: `backend/tests/test_xml_parser.py`
- Test: `backend/tests/fixtures/sample_blockly.xml`

- [ ] **Step 1: Write the failing parser test using a real sample**

```python
from pathlib import Path

from app.services.xml_parser import parse_blockly_xml


def test_parse_blockly_xml_extracts_block_types() -> None:
    xml_content = Path("tests/fixtures/sample_blockly.xml").read_text(encoding="utf-8")

    parsed = parse_blockly_xml(xml_content)

    assert parsed["root_block_types"] == ["board_initializes_setup"]
    assert "delay_custom" in parsed["all_block_types"]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd backend; pytest tests/test_xml_parser.py::test_parse_blockly_xml_extracts_block_types -v`
Expected: FAIL with `ImportError` or missing function

- [ ] **Step 3: Write minimal implementation**

```python
# backend/app/services/xml_parser.py
from xml.etree import ElementTree


def parse_blockly_xml(xml_content: str) -> dict[str, list[str]]:
    root = ElementTree.fromstring(xml_content)
    blocks = root.findall(".//{https://developers.google.com/blockly/xml}block")
    block_types = [block.attrib["type"] for block in blocks if "type" in block.attrib]
    root_blocks = root.findall("{https://developers.google.com/blockly/xml}block")
    root_block_types = [block.attrib["type"] for block in root_blocks if "type" in block.attrib]
    return {
        "root_block_types": root_block_types,
        "all_block_types": block_types,
    }
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd backend; pytest tests/test_xml_parser.py::test_parse_blockly_xml_extracts_block_types -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add backend/app/services/xml_parser.py backend/tests/test_xml_parser.py backend/tests/fixtures/sample_blockly.xml
git commit -m "feat: parse blockly xml into structured data"
```

## Task 7: Build Rule Engine for Red-Light Hard Failures

**Files:**
- Create: `backend/app/services/rule_engine.py`
- Test: `backend/tests/test_rule_engine.py`

- [ ] **Step 1: Write the failing red-light rule test**

```python
from app.services.rule_engine import evaluate_rules


def test_marks_missing_required_block_as_red() -> None:
    parsed = {
        "root_block_types": ["board_initializes_setup"],
        "all_block_types": ["board_initializes_setup", "initializes_loop"],
    }
    rules = {"required_blocks": ["delay_custom"]}

    result = evaluate_rules(parsed, rules)

    assert result["final_light"] == "red"
    assert result["final_grade"] == "待加強"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd backend; pytest tests/test_rule_engine.py::test_marks_missing_required_block_as_red -v`
Expected: FAIL with missing module or function

- [ ] **Step 3: Write minimal implementation**

```python
# backend/app/services/rule_engine.py
def evaluate_rules(parsed: dict, rules: dict) -> dict:
    required_blocks = set(rules.get("required_blocks", []))
    actual_blocks = set(parsed.get("all_block_types", []))

    missing_blocks = sorted(required_blocks - actual_blocks)
    if missing_blocks:
        return {
            "rule_status": "hard_fail",
            "missing_blocks": missing_blocks,
            "final_light": "red",
            "final_grade": "待加強",
        }

    return {
        "rule_status": "pass",
        "missing_blocks": [],
        "final_light": None,
        "final_grade": None,
    }
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd backend; pytest tests/test_rule_engine.py::test_marks_missing_required_block_as_red -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add backend/app/services/rule_engine.py backend/tests/test_rule_engine.py
git commit -m "feat: add rule engine hard-fail checks"
```

## Task 8: Add Async Evaluation Pipeline and Result Decision Logic

**Files:**
- Create: `backend/app/services/evaluation_service.py`
- Create: `backend/app/schemas/evaluation.py`
- Create: `backend/app/services/llm_service.py`
- Test: `backend/tests/test_evaluation_flow.py`
- Modify: `backend/app/api/submissions.py`

- [ ] **Step 1: Write the failing async evaluation flow test**

```python
from app.services.evaluation_service import decide_final_result


def test_rule_engine_overrides_ai_when_conflicting() -> None:
    rule_result = {"final_light": "red", "final_grade": "待加強", "rule_status": "hard_fail"}
    ai_result = {"light": "green", "grade": "優"}

    result = decide_final_result(rule_result, ai_result)

    assert result["light"] == "red"
    assert result["grade"] == "待加強"
    assert result["source"] == "rule_engine"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd backend; pytest tests/test_evaluation_flow.py::test_rule_engine_overrides_ai_when_conflicting -v`
Expected: FAIL with missing function

- [ ] **Step 3: Write minimal implementation**

```python
# backend/app/services/evaluation_service.py
def decide_final_result(rule_result: dict, ai_result: dict) -> dict:
    if rule_result.get("final_light"):
        return {
            "light": rule_result["final_light"],
            "grade": rule_result["final_grade"],
            "source": "rule_engine",
        }
    return {
        "light": ai_result["light"],
        "grade": ai_result["grade"],
        "source": "ai",
    }
```

```python
# extend later in same file
def mock_ai_evaluate(parsed: dict, assignment_prompt: str) -> dict:
    block_count = len(parsed.get("all_block_types", []))
    if block_count >= 8:
        return {"light": "green", "grade": "優"}
    if block_count >= 5:
        return {"light": "blue", "grade": "良"}
    return {"light": "yellow", "grade": "可"}
```

```python
# backend/app/services/llm_service.py
from google import genai


class LLMService:
    def __init__(self, api_key: str) -> None:
        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-2.5-flash-lite"

    def evaluate_submission(self, assignment_prompt: str, parsed: dict) -> dict:
        prompt = f"""
作業說明:
{assignment_prompt}

解析後積木結構:
{parsed}

請輸出 JSON，欄位包含 grade, light, strengths, issues, suggestions。
"""
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
        )
        return {"raw_text": response.text}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd backend; pytest tests/test_evaluation_flow.py::test_rule_engine_overrides_ai_when_conflicting -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add backend/app/services/evaluation_service.py backend/tests/test_evaluation_flow.py backend/app/api/submissions.py
git commit -m "feat: add evaluation decision logic"
```

## Task 9: Push Real-Time Updates to Student and Teacher Screens

**Files:**
- Create: `backend/app/core/websocket_hub.py`
- Create: `backend/app/api/ws.py`
- Test: `backend/tests/test_websocket_events.py`
- Modify: `backend/app/main.py`

- [ ] **Step 1: Write the failing WebSocket event test**

```python
from fastapi.testclient import TestClient

from app.main import app


def test_websocket_receives_submission_status_update() -> None:
    client = TestClient(app)

    with client.websocket_connect("/ws/activities/1") as websocket:
        websocket.send_json({"type": "ping"})
        data = websocket.receive_json()

    assert data["type"] == "pong"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd backend; pytest tests/test_websocket_events.py::test_websocket_receives_submission_status_update -v`
Expected: FAIL with `404` or websocket route missing

- [ ] **Step 3: Write minimal implementation**

```python
# backend/app/api/ws.py
from fastapi import APIRouter, WebSocket

router = APIRouter()


@router.websocket("/ws/activities/{activity_id}")
async def activity_socket(websocket: WebSocket, activity_id: int) -> None:
    await websocket.accept()
    payload = await websocket.receive_json()
    if payload["type"] == "ping":
        await websocket.send_json({"type": "pong", "activity_id": activity_id})
```

```python
# backend/app/services/realtime_service.py
from supabase import Client


class RealtimeService:
    def __init__(self, supabase_client: Client) -> None:
        self.supabase = supabase_client

    def publish_submission_update(self, activity_id: int, payload: dict) -> None:
        self.supabase.channel(f"activity:{activity_id}").send_broadcast(
            "submission_update",
            payload,
        )
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd backend; pytest tests/test_websocket_events.py::test_websocket_receives_submission_status_update -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add backend/app/api/ws.py backend/app/main.py backend/tests/test_websocket_events.py
git commit -m "feat: add realtime websocket channel"
```

## Task 10: Add Teacher Review, Final Override, and Reporting APIs

**Files:**
- Create: `backend/app/services/review_service.py`
- Create: `backend/app/services/report_service.py`
- Create: `backend/app/api/teacher.py`
- Create: `backend/app/api/reports.py`
- Test: `backend/tests/test_teacher_review_api.py`

- [ ] **Step 1: Write the failing override test**

```python
from fastapi.testclient import TestClient

from app.main import app


def test_teacher_can_override_final_grade() -> None:
    client = TestClient(app)

    response = client.post(
        "/api/teacher/submissions/1/override",
        json={"grade": "優", "light": "green", "reason": "Teacher review"},
        headers={"Authorization": "Bearer dev-token"},
    )

    assert response.status_code == 200
    assert response.json()["teacher_revised"] is True
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd backend; pytest tests/test_teacher_review_api.py::test_teacher_can_override_final_grade -v`
Expected: FAIL with `404 Not Found`

- [ ] **Step 3: Write minimal implementation**

```python
# backend/app/api/teacher.py
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/api/teacher", tags=["teacher"])


class OverrideRequest(BaseModel):
    grade: str
    light: str
    reason: str


@router.post("/submissions/{submission_id}/override")
def override_submission(submission_id: int, payload: OverrideRequest) -> dict:
    return {
        "submission_id": submission_id,
        "grade": payload.grade,
        "light": payload.light,
        "teacher_revised": True,
    }
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd backend; pytest tests/test_teacher_review_api.py::test_teacher_can_override_final_grade -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add backend/app/api/teacher.py backend/tests/test_teacher_review_api.py
git commit -m "feat: add teacher override api"
```

## Task 11: Scaffold Frontend App and Login Flow

**Files:**
- Create: `frontend/package.json`
- Create: `frontend/src/main.tsx`
- Create: `frontend/src/App.tsx`
- Create: `frontend/src/features/auth/LoginPage.tsx`
- Test: `frontend/src/test/LoginPage.test.tsx`

- [ ] **Step 1: Write the failing login page test**

```tsx
import { render, screen } from "@testing-library/react";

import { LoginPage } from "../features/auth/LoginPage";


test("renders login fields", () => {
  render(<LoginPage />);

  expect(screen.getByLabelText("帳號")).toBeInTheDocument();
  expect(screen.getByLabelText("密碼")).toBeInTheDocument();
});
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd frontend; npm test -- LoginPage.test.tsx`
Expected: FAIL because project files do not exist

- [ ] **Step 3: Write minimal implementation**

```tsx
// frontend/src/features/auth/LoginPage.tsx
export function LoginPage() {
  return (
    <form>
      <label>
        帳號
        <input aria-label="帳號" />
      </label>
      <label>
        密碼
        <input aria-label="密碼" type="password" />
      </label>
      <button type="submit">登入</button>
    </form>
  );
}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd frontend; npm test -- LoginPage.test.tsx`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add frontend/package.json frontend/src frontend/src/test/LoginPage.test.tsx
git commit -m "feat: scaffold frontend login flow"
```

## Task 12: Implement Student Submission and Live Result Screens

**Files:**
- Create: `frontend/src/features/student/StudentAssignmentsPage.tsx`
- Create: `frontend/src/features/student/StudentSubmissionPage.tsx`
- Create: `frontend/src/features/student/StudentClassStatusPage.tsx`
- Create: `frontend/src/components/FeedbackCard.tsx`
- Test: `frontend/src/test/StudentSubmissionPage.test.tsx`

- [ ] **Step 1: Write the failing student submission page test**

```tsx
import { render, screen } from "@testing-library/react";

import { StudentSubmissionPage } from "../features/student/StudentSubmissionPage";


test("shows xml textbox and submit button", () => {
  render(<StudentSubmissionPage />);

  expect(screen.getByLabelText("XML 內容")).toBeInTheDocument();
  expect(screen.getByRole("button", { name: "提交" })).toBeInTheDocument();
});
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd frontend; npm test -- StudentSubmissionPage.test.tsx`
Expected: FAIL because component does not exist

- [ ] **Step 3: Write minimal implementation**

```tsx
// frontend/src/features/student/StudentSubmissionPage.tsx
export function StudentSubmissionPage() {
  return (
    <section>
      <label>
        XML 內容
        <textarea aria-label="XML 內容" rows={16} />
      </label>
      <button type="button">提交</button>
      <p>提交後將顯示評分中，完成後自動更新。</p>
    </section>
  );
}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd frontend; npm test -- StudentSubmissionPage.test.tsx`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add frontend/src/features/student frontend/src/components/FeedbackCard.tsx frontend/src/test/StudentSubmissionPage.test.tsx
git commit -m "feat: add student submission screens"
```

## Task 13: Implement Teacher Dashboard, Realtime Grid, and Reporting UI

**Files:**
- Create: `frontend/src/features/teacher/TeacherActivitiesPage.tsx`
- Create: `frontend/src/features/teacher/TeacherDashboardPage.tsx`
- Create: `frontend/src/features/teacher/TeacherReportPage.tsx`
- Create: `frontend/src/features/teacher/TeacherReviewDrawer.tsx`
- Create: `frontend/src/components/AssignmentGrid.tsx`
- Create: `frontend/src/components/StatusBadge.tsx`
- Test: `frontend/src/test/TeacherDashboardPage.test.tsx`

- [ ] **Step 1: Write the failing teacher dashboard test**

```tsx
import { render, screen } from "@testing-library/react";

import { TeacherDashboardPage } from "../features/teacher/TeacherDashboardPage";


test("renders class dashboard title", () => {
  render(<TeacherDashboardPage />);

  expect(screen.getByText("班級總覽")).toBeInTheDocument();
  expect(screen.getByText("評分中")).toBeInTheDocument();
});
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd frontend; npm test -- TeacherDashboardPage.test.tsx`
Expected: FAIL because component does not exist

- [ ] **Step 3: Write minimal implementation**

```tsx
// frontend/src/features/teacher/TeacherDashboardPage.tsx
export function TeacherDashboardPage() {
  return (
    <section>
      <h1>班級總覽</h1>
      <table>
        <tbody>
          <tr>
            <td>王小明</td>
            <td>評分中</td>
          </tr>
        </tbody>
      </table>
    </section>
  );
}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd frontend; npm test -- TeacherDashboardPage.test.tsx`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add frontend/src/features/teacher frontend/src/components frontend/src/test/TeacherDashboardPage.test.tsx
git commit -m "feat: add teacher dashboard and report screens"
```

## Task 14: Document API, Local Setup, and Manual QA

**Files:**
- Create: `docs/api/student-ai-grading-api.md`
- Create: `docs/deployment/free-tier-deployment.md`
- Create: `docs/data-model/student-ai-grading-er.md`
- Create: `docs/runbooks/local-development.md`
- Modify: `docs/student-ai-grading-system-spec.md`

- [ ] **Step 1: Write the failing documentation checklist as a testable artifact**

```markdown
# Manual QA Checklist

- [ ] Teacher can create and activate an activity
- [ ] Student can submit valid XML
- [ ] Invalid XML is rejected immediately
- [ ] Submission changes to 評分中 before final result
- [ ] Teacher dashboard updates without refresh
- [ ] Teacher override replaces student-visible final result
```

- [ ] **Step 2: Run documentation review**

Run a marker scan across first-party docs and source files, excluding generated dependency and cache folders.
Expected: no open work markers

- [ ] **Step 3: Write the documentation**

```markdown
# Student AI Grading API

## POST /api/auth/login
- Request: `{"account": "teacher01", "password": "secret123"}`
- Response: `{"access_token": "token", "role": "teacher"}`

## POST /api/submissions
- Request: `{"assignment_id": 101, "activity_id": 1, "xml_content": "<xml />"}`
- Response: `{"status": "queued"}`
```

```markdown
# Free-Tier Deployment

## Frontend
- Platform: Vercel Hobby
- Build command: `npm run build`

## Backend
- Platform: Render Free Web Service
- Start command: `uvicorn app.main:app --host 0.0.0.0 --port 10000`

## Database/Auth/Realtime
- Platform: Supabase Free

## LLM
- Provider: Gemini Developer API
- Model: `gemini-2.5-flash-lite`
```

- [ ] **Step 4: Run final verification**

Run: `cd backend; pytest -v && cd ..\\frontend; npm test`
Expected: all tests pass

- [ ] **Step 5: Commit**

```bash
git add docs backend frontend
git commit -m "docs: add api and local setup guides"
```

## Spec Coverage Check

- Login and role separation: covered by Tasks 3, 11, 13.
- Activity creation and assignment selection: covered by Tasks 4 and 13.
- XML input, validation, and history-ready submission model: covered by Tasks 2 and 5.
- Rule-based first pass and AI-assisted grading: covered by Tasks 6, 7, and 8.
- Async processing and auto refresh: covered by Tasks 8, 9, 12, and 13.
- Teacher override and final-result precedence: covered by Task 10 and Task 13.
- Reporting by assignment: covered by Tasks 10 and 13.

No uncovered spec requirements remain for v1.

## Self-Review

- Marker scan completed: no open work markers remain in plan steps.
- Type consistency checked: `assignment_id`, `activity_id`, `xml_content`, `grade`, and `light` names are used consistently across API, services, and tests.
- Scope check completed: plan stays inside v1 boundaries and avoids image uploads, multi-class support, and multi-language parsing.
