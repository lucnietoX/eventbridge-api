#  EventBridge API — Event-Driven Webhook Integration Service
An event-driven backend service built with FastAPI to ingest, persist, process, and route webhook events **asynchronously**. The system is designed to simulate real world payment integrations (in this case, **Stripe**).

Payment providers, CRMs, e-commerce platforms and SaaS tools emit webhooks that must be:
- received quickly
- stored safely
- processed asynchronously
- routed to downstream systems

This project demonstrates how to build such a system correctly, without over-engineering.

### Architectural style
- Event-driven monolith
- Layered architecture (API → Services → Integrations → DB)
- Designed to evolve into queue-based workers if needed

### Tech Stack

- Python 3.11
- FastAPI
- PostgreSQL
- SQLAlchemy (Async)
- Alembic
- httpx (async HTTP client)
- Notion API
- Stripe Webhooks (Test Mode)
- Docker
- Fly.io


### Project Structure

```
eventbridge-api/
│
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entrypoint
│   ├── api/
│   │   └── v1/
│   │       ├── webhooks/        # Webhook endpoints
│   │       └── executions.py    # Retry & execution management endpoints
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py            # Environment & app configuration
│   ├── db/
│   │   ├── __init__.py
│   │   ├── database.py          # Async SQLAlchemy engine & session
│   │   ├── deps.py              # FastAPI DB dependencies
│   │   └── models.py            # ORM models (Event, Execution)
│   ├── log/
│   │   ├── __init__.py
│   │   └── logger_setup.py      # Application logging configuration
│   ├── services/
│   │   ├── __init__.py
│   │   ├── executor.py          # Background execution orchestration
│   │   └── notion/
│   │       ├── __init__.py
│   │       ├── executor_notion.py  # Notion-specific execution logic
│   │       └── notion_payments.py  # Notion API client & payload mapping
│   └── support/
│       ├── __init__.py
│       └── utils.py             # Shared helper utilities
├── migrations/
│   ├── env.py                   # Alembic migration environment
│   ├── script.py.mako
│   └── versions/                # Auto-generated DB migrations
├── docker-compose.yml           # Local development stack (API + Postgres)
├── Dockerfile                   # Production container image
├── alembic.ini                  # Alembic configuration
├── requirements.txt             # Python dependencies
├── .env                         # Local environment variables (gitignored)
├── .env-model                   # Environment variable template
├── .gitignore
├── README.md
└── LICENSE
```

### Reference
- https://developers.notion.com/reference/post-page
- https://docs.stripe.com/api/payment_intents/object
- https://docs.stripe.com/api

# License
```
This project is licensed under the MIT License. See the [LICENSE] file for details.

Author: Luciano Nieto
```