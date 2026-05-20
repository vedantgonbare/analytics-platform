from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.websocket_manager import manager

router = APIRouter()

@router.websocket("/analytics")
async def websocket_analytics(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        # Keep connection alive, listen for client messages
        while True:
            data = await websocket.receive_text()
            # Echo back a pong to keep alive
            await websocket.send_json({"type": "pong", "message": data})
    except WebSocketDisconnect:
        manager.disconnect(websocket)