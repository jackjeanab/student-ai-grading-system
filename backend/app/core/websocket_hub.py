from collections import defaultdict
from typing import DefaultDict

from fastapi import WebSocket


class WebSocketHub:
    def __init__(self) -> None:
        self._activity_connections: DefaultDict[int, set[WebSocket]] = defaultdict(set)

    async def connect(self, activity_id: int, websocket: WebSocket) -> None:
        await websocket.accept()
        self._activity_connections[activity_id].add(websocket)

    def disconnect(self, activity_id: int, websocket: WebSocket) -> None:
        connections = self._activity_connections.get(activity_id)
        if connections is None:
            return

        connections.discard(websocket)
        if not connections:
            self._activity_connections.pop(activity_id, None)

    async def send_activity_event(self, activity_id: int, payload: dict[str, object]) -> None:
        connections = list(self._activity_connections.get(activity_id, set()))
        for websocket in connections:
            try:
                await websocket.send_json(payload)
            except Exception:
                self.disconnect(activity_id, websocket)


websocket_hub = WebSocketHub()
