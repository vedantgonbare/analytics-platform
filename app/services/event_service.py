import json
from app.db.redis import redis_client

EVENTS_QUEUE = "events:queue"

async def push_event_to_queue(event_data: dict) -> int:
    """Push event to Redis list queue. Returns queue length."""
    payload = json.dumps(event_data, default=str)
    queue_length = await redis_client.lpush(EVENTS_QUEUE, payload)
    return queue_length

async def get_queue_length() -> int:
    return await redis_client.llen(EVENTS_QUEUE)