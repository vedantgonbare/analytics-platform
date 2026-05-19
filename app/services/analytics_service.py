from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select
from datetime import datetime, timedelta
from app.models.event import Event

async def get_summary(db: AsyncSession) -> dict:
    result = await db.execute(
        select(
            func.count(Event.id).label("total_events"),
            func.count(func.distinct(Event.user_id)).label("unique_users"),
            func.count(func.distinct(Event.session_id)).label("unique_sessions"),
        )
    )
    row = result.one()
    return {
        "total_events": row.total_events,
        "unique_users": row.unique_users,
        "unique_sessions": row.unique_sessions,
    }

async def get_events_by_type(db: AsyncSession) -> list:
    result = await db.execute(
        select(
            Event.event_type,
            func.count(Event.id).label("count"),
        )
        .group_by(Event.event_type)
        .order_by(func.count(Event.id).desc())
    )
    return [{"event_type": row.event_type, "count": row.count} for row in result]

async def get_events_over_time(db: AsyncSession, hours: int = 24) -> list:
    since = datetime.utcnow() - timedelta(hours=hours)
    result = await db.execute(
        select(
            func.date_trunc("hour", Event.timestamp).label("hour"),
            func.count(Event.id).label("count"),
        )
        .where(Event.timestamp >= since)
        .group_by(func.date_trunc("hour", Event.timestamp))
        .order_by(func.date_trunc("hour", Event.timestamp))
    )
    return [
        {"hour": str(row.hour), "count": row.count}
        for row in result
    ]

async def get_top_pages(db: AsyncSession, limit: int = 10) -> list:
    result = await db.execute(
        select(
            Event.page,
            func.count(Event.id).label("views"),
            func.count(func.distinct(Event.user_id)).label("unique_users"),
        )
        .where(Event.page.isnot(None))
        .group_by(Event.page)
        .order_by(func.count(Event.id).desc())
        .limit(limit)
    )
    return [
        {"page": row.page, "views": row.views, "unique_users": row.unique_users}
        for row in result
    ]