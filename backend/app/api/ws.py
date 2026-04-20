from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.core.websocket_hub import websocket_hub

router = APIRouter(tags=["websocket"])


@router.websocket("/ws/activities/{activity_id}")
async def activity_events(websocket: WebSocket, activity_id: int) -> None:
    await websocket_hub.connect(activity_id, websocket)
    try:
        while True:
            message = await websocket.receive_text()
            if message == "ping":
                await websocket.send_text("pong")
            else:
                await websocket.send_text("unsupported_message")
    except WebSocketDisconnect:
        pass
    finally:
        websocket_hub.disconnect(activity_id, websocket)
