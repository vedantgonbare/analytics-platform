import json
import asyncio
from datetime import datetime
from app.db.database import AsyncSessionLocal
from app.db.redis import redis_client
from app.models.event import Event

EVENTS_QUEUE = "events:queue"
EVENTS_CHANNEL = "events:live"

async def process_event(event_data: dict):
    async with AsyncSessionLocal() as session:
        event = Event(
            event_type=event_data.get("event_type"),
            user_id=event_data.get("user_id"),
            session_id=event_data.get("session_id"),
            page=event_data.get("page"),
            properties=event_data.get("properties"),
            timestamp=datetime.fromisoformat(event_data["timestamp"])
            if event_data.get("timestamp")
            else datetime.utcnow(),
        )
        session.add(event)
        await session.commit()
        await session.refresh(event)
        print(f"[Worker] Processed event: {event.event_type} | id: {event.id}")

        # Publish to Redis channel instead of broadcasting directly
        message = json.dumps({
            "type": "new_event",
            "event_type": event.event_type,
            "user_id": event.user_id,
            "page": event.page,
            "timestamp": str(event.timestamp),
        })
        await redis_client.publish(EVENTS_CHANNEL, message)
        print(f"[Worker] Published to Redis channel: {EVENTS_CHANNEL}")

async def run_worker():
    print("[Worker] Starting... listening on queue:", EVENTS_QUEUE)
    while True:
        try:
            result = await redis_client.brpop(EVENTS_QUEUE, timeout=5)
            if result:
                _, payload = result
                event_data = json.loads(payload)
                await process_event(event_data)
        except Exception as e:
            print(f"[Worker] Error: {e}")
            await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(run_worker())