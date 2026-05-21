from fastapi import APIRouter, Request, status
from slowapi import Limiter
from slowapi.util import get_remote_address
from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime
from app.services.event_service import push_event_to_queue

limiter = Limiter(key_func=get_remote_address)
router = APIRouter()

class EventCreate(BaseModel):
    event_type: str
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    page: Optional[str] = None
    properties: Optional[Dict[str, Any]] = None
    timestamp: Optional[datetime] = None

class EventQueued(BaseModel):
    status: str
    message: str
    queue_length: int

@router.post("/", response_model=EventQueued, status_code=status.HTTP_202_ACCEPTED)
@limiter.limit("100/minute")
async def ingest_event(request: Request, payload: EventCreate):
    event_data = {
        "event_type": payload.event_type,
        "user_id": payload.user_id,
        "session_id": payload.session_id,
        "page": payload.page,
        "properties": payload.properties,
        "timestamp": payload.timestamp.isoformat() if payload.timestamp else None,
    }
    queue_length = await push_event_to_queue(event_data)
    return EventQueued(
        status="queued",
        message=f"Event '{payload.event_type}' accepted for processing",
        queue_length=queue_length,
    )