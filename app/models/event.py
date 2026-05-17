import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, JSON, Index
from sqlalchemy.dialects.postgresql import UUID
from app.db.database import Base

class Event(Base):
    __tablename__ = "events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_type = Column(String(100), nullable=False)        # "click", "page_view", etc.
    user_id = Column(String(255), nullable=True)            # anonymous or logged-in
    session_id = Column(String(255), nullable=True)
    page = Column(String(500), nullable=True)               # "/home", "/product/123"
    properties = Column(JSON, nullable=True)                # any extra data
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    __table_args__ = (
        Index("ix_events_event_type", "event_type"),
        Index("ix_events_timestamp", "timestamp"),
        Index("ix_events_user_id", "user_id"),
    )