# 🚀 Real-Time Analytics Platform

A production-grade backend built with FastAPI that ingests events, processes them via a Redis queue, stores aggregated data in PostgreSQL, and pushes live updates via WebSockets.

## Tech Stack

| Layer | Technology |
|---|---|
| API | FastAPI + WebSockets |
| Database | PostgreSQL (SQLAlchemy async) |
| Cache / Queue | Redis |
| Background Worker | Python asyncio |
| Auth | JWT (python-jose + bcrypt) |
| Migrations | Alembic |
| Containerization | Docker + docker-compose |
| Testing | pytest + httpx |

## Architecture

```
Client → POST /api/v1/events/
              ↓
         Redis Queue
              ↓
      Background Worker → PostgreSQL
              ↓
        Redis Pub/Sub
              ↓
       WebSocket Clients (live updates)
```

## Features

- ✅ Event ingestion API (click, page_view, sign_up, etc.)
- ✅ Async Redis queue for high-throughput ingestion
- ✅ Background worker for DB persistence
- ✅ Analytics query API (summary, by-type, over-time, top-pages)
- ✅ Real-time WebSocket broadcast via Redis Pub/Sub
- ✅ JWT authentication (register, login, protected routes)
- ✅ Rate limiting (100 requests/minute on ingest)
- ✅ Docker + docker-compose setup
- ✅ Pytest test suite

## Getting Started

### Prerequisites
- Docker Desktop
- Python 3.11+

### Run with Docker
```bash
docker-compose up --build
```

### Run locally
```bash
# Start dependencies
docker-compose up postgres redis -d

# Install dependencies
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Terminal 1 - API
uvicorn app.main:app --reload

# Terminal 2 - Worker
python -m app.services.worker
```

## API Endpoints

### Auth
| Method | Endpoint | Description |
|---|---|---|
| POST | /api/v1/auth/register | Register new user |
| POST | /api/v1/auth/login | Login + get JWT token |
| GET | /api/v1/auth/me | Get current user |

### Events
| Method | Endpoint | Description |
|---|---|---|
| POST | /api/v1/events/ | Ingest event (rate limited) |

### Analytics (🔒 JWT required)
| Method | Endpoint | Description |
|---|---|---|
| GET | /api/v1/analytics/summary | Total events, users, sessions |
| GET | /api/v1/analytics/events-by-type | Count per event type |
| GET | /api/v1/analytics/events-over-time | Count per hour (last 24h) |
| GET | /api/v1/analytics/top-pages | Most visited pages |

### WebSocket
| Endpoint | Description |
|---|---|
| ws://localhost:8000/ws/analytics | Live event stream |

## Running Tests
```bash
pytest tests/ -v
```

## Project Structure
```
analytics-platform/
├── app/
│   ├── api/          # Route handlers
│   ├── core/         # Config, security, dependencies
│   ├── db/           # Database + Redis connections
│   ├── models/       # SQLAlchemy models
│   └── services/     # Business logic + worker
├── alembic/          # DB migrations
├── tests/            # Pytest test suite
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```