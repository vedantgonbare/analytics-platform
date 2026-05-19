from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from pydantic import BaseModel

from app.db.database import get_db
from app.services.analytics_service import (
    get_summary,
    get_events_by_type,
    get_events_over_time,
    get_top_pages,
)

router = APIRouter()

# --- Response Schemas ---
class SummaryResponse(BaseModel):
    total_events: int
    unique_users: int
    unique_sessions: int

class EventByTypeResponse(BaseModel):
    event_type: str
    count: int

class EventOverTimeResponse(BaseModel):
    hour: str
    count: int

class TopPageResponse(BaseModel):
    page: str
    views: int
    unique_users: int

# --- Endpoints ---
@router.get("/summary", response_model=SummaryResponse)
async def summary(db: AsyncSession = Depends(get_db)):
    return await get_summary(db)

@router.get("/events-by-type", response_model=List[EventByTypeResponse])
async def events_by_type(db: AsyncSession = Depends(get_db)):
    return await get_events_by_type(db)

@router.get("/events-over-time", response_model=List[EventOverTimeResponse])
async def events_over_time(
    hours: int = Query(default=24, ge=1, le=168),
    db: AsyncSession = Depends(get_db),
):
    return await get_events_over_time(db, hours=hours)

@router.get("/top-pages", response_model=List[TopPageResponse])
async def top_pages(
    limit: int = Query(default=10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    return await get_top_pages(db, limit=limit)