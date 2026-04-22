from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.core.rate_limit import InMemoryRateLimitMiddleware


def test_rate_limit_protects_submission_routes_only() -> None:
    app = FastAPI()
    app.add_middleware(InMemoryRateLimitMiddleware, requests_per_minute=1)

    @app.post("/api/submissions")
    def submit() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    client = TestClient(app)

    assert client.post("/api/submissions").status_code == 200
    assert client.post("/api/submissions").status_code == 429
    assert client.get("/health").status_code == 200
