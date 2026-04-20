from fastapi.testclient import TestClient

from app.core.websocket_hub import WebSocketHub
from app.main import app


def test_activity_websocket_responds_to_ping() -> None:
    client = TestClient(app)

    with client.websocket_connect("/ws/activities/42") as websocket:
        websocket.send_text("ping")

        assert websocket.receive_text() == "pong"


def test_activity_websocket_signals_unsupported_messages() -> None:
    client = TestClient(app)

    with client.websocket_connect("/ws/activities/42") as websocket:
        websocket.send_text("hello")

        assert websocket.receive_text() == "unsupported_message"


def test_websocket_hub_prunes_failed_connections() -> None:
    class FakeWebSocket:
        def __init__(self, should_fail: bool) -> None:
            self.should_fail = should_fail

        async def accept(self) -> None:
            return None

        async def send_json(self, payload: dict[str, object]) -> None:
            if self.should_fail:
                raise RuntimeError("connection closed")

    hub = WebSocketHub()
    healthy = FakeWebSocket(False)
    stale = FakeWebSocket(True)

    import asyncio

    async def run() -> None:
        await hub.connect(7, healthy)
        await hub.connect(7, stale)
        await hub.send_activity_event(7, {"status": "broadcast"})

    asyncio.run(run())

    assert hub._activity_connections[7] == {healthy}
