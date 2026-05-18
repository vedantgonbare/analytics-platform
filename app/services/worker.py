import json
import asyncio
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import AsyncSessionLocal
from app.db.redis import redis_client
from app.models.event import Event

EVENTS_QUEUE = "events:queue"

async def process_event(event_data: dict):
    """Write a single event to PostgreSQL."""
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
        print(f"[Worker] Processed event: {event.event_type} | id: {event.id}")

async def run_worker():
    """Continuously poll Redis queue and process events."""
    print("[Worker] Starting... listening on queue:", EVENTS_QUEUE)
    while True:
        try:
            # BRPOP blocks up to 5s waiting for an item
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