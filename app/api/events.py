from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

from app.db.database import get_db
from app.models.event import Event

router = APIRouter()

# --- Request Schema ---
class EventCreate(BaseModel):
    event_type: str
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    page: Optional[str] = None
    properties: Optional[Dict[str, Any]] = None
    timestamp: Optional[datetime] = None

# --- Response Schema ---
class EventResponse(BaseModel):
    id: str
    event_type: str
    user_id: Optional[str]
    session_id: Optional[str]
    page: Optional[str]
    properties: Optional[Dict[str, Any]]
    timestamp: datetime

    class Config:
        from_attributes = True

# --- POST /api/v1/events ---
@router.post("/", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
async def ingest_event(payload: EventCreate, db: AsyncSession = Depends(get_db)):
    event = Event(
        event_type=payload.event_type,
        user_id=payload.user_id,
        session_id=payload.session_id,
        page=payload.page,
        properties=payload.properties,
        timestamp=payload.timestamp or datetime.utcnow(),
    )
    db.add(event)
    await db.commit()
    await db.refresh(event)

    return EventResponse(
        id=str(event.id),
        event_type=event.event_type,
        user_id=event.user_id,
        session_id=event.session_id,
        page=event.page,
        properties=event.properties,
        timestamp=event.timestamp,
    )