from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.websocket_manager import manager
from app.db.redis import redis_client
import asyncio
import json

router = APIRouter()

@router.websocket("/analytics")
async def websocket_analytics(websocket: WebSocket):
    await manager.connect(websocket)

    # Create a separate Redis connection for pub/sub
    pubsub = redis_client.pubsub()
    await pubsub.subscribe("events:live")

    async def listen_redis():
        async for message in pubsub.listen():
            if message["type"] == "message":
                data = json.loads(message["data"])
                await websocket.send_json(data)

    # Run Redis listener as background task
    redis_task = asyncio.create_task(listen_redis())

    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_json({"type": "pong", "message": data})
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        redis_task.cancel()
        await pubsub.unsubscribe("events:live")