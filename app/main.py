from fastapi import FastAPI
from app.api import events, analytics, websocket

app = FastAPI(title="Analytics Platform", version="1.0.0")

app.include_router(events.router, prefix="/api/v1/events", tags=["events"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["analytics"])
app.include_router(websocket.router, prefix="/ws", tags=["websocket"])

@app.get("/health")
async def health():
    return {"status": "ok"}