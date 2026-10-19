# Dump Tasks

A backend API that turns messy input (plain text lists, emails, voice-note transcripts) into a clean, actionable to-do list. You "dump" raw text, and an AI model extracts the tasks, due dates and effort estimates. Later versions split big tasks into micro-tasks and let you search your tasks by meaning using embeddings.

Built with FastAPI, SQLAlchemy, PostgreSQL (with pgvector) and the Gemini API, entirely on free-tier tools.

> **Status:** early development. The foundation, database schema and the first AI ingestion flow are in place. See the [roadmap](#roadmap).

## Why this project exists

This is a learning project. The goals are:

- Clean backend architecture: routers, services, repositories and models, each with one job.
- Integrating an AI model: structured output validated with Pydantic, prompt design and error handling.
- Embeddings and semantic search with pgvector.
- Database migrations with Alembic.
- Testing, linting and CI habits (pytest, ruff).
- Building our own authentication (planned).

## Tech stack

| Area | Choice |
|---|---|
| Language | Python 3.10+ |
| API framework | FastAPI, served by Uvicorn |
| Database | PostgreSQL (Supabase free tier) with the `pgvector` extension |
| ORM and migrations | SQLAlchemy 2.x, Alembic, `psycopg` 3 |
| AI | Gemini API through the `google-genai` SDK |
| Validation | Pydantic |
| Tooling | pytest, ruff, uv (used to compile the requirements files) |

## Project structure

```
dump_tasks/
├── main.py                  # FastAPI app: routers, error handlers, /system-status
├── database.py              # DB URL loading, engine, session factory, Base, get_db
├── alembic/                 # Migration environment and versions
├── app/
│   ├── core/                # App-wide plumbing: dependencies, exceptions, error handlers
│   ├── models/              # SQLAlchemy tables (structure only)
│   ├── schemas/             # Pydantic request/response shapes
│   ├── repositories/        # The only code that talks to the database
│   ├── services/            # Business logic and orchestration
│   ├── clients/             # Wrappers around external APIs (Gemini)
│   └── routers/             # HTTP endpoints
├── tests/
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
└── Procfile
```

### Layer rules

Each layer only does its own job and only talks to the layer below it: `router → service → repository → model`.

| Layer | Responsible for | Must not contain |
|---|---|---|
| `routers/` | HTTP: routes, status codes, passing data to a service | Business rules, validation logic, SQL |
| `schemas/` | The shape and types of request and response data | Business rules |
| `services/` | Business rules, decisions, orchestration, transaction commit | SQL, HTTP details |
| `repositories/` | Database queries and writes (flush only) | Business rules |
| `clients/` | Talking to external APIs such as Gemini | Database access |
| `models/` | Table definitions | Logic |

Services raise plain errors (`NotFoundError`, `ConflictError`, `ExternalServiceError`) from `app/core/exceptions.py`. `app/core/error_handlers.py` turns them into HTTP responses in one place.

## Getting started

### Prerequisites

- Python 3.10 or newer
- A PostgreSQL database with the `pgvector` extension. The easiest free option is a [Supabase](https://supabase.com) project.
- A Gemini API key from [Google AI Studio](https://aistudio.google.com)

### 1. Clone and install

```bash
git clone https://github.com/<your-username>/dump_tasks.git
cd dump_tasks
python -m venv env
source env/bin/activate
pip install -r requirements-dev.txt
```

### 2. Configure environment variables

Copy the example file and fill it in:

```bash
cp .env.example .env
```

| Variable | Description |
|---|---|
| `DATABASE_URL` | PostgreSQL connection string. `postgres://` and `postgresql://` are converted to the `postgresql+psycopg://` form automatically. |
| `GEMINI_API_KEY` | Your Gemini API key. Only needed when calling the AI endpoints. |

Notes on `DATABASE_URL`:

- With Supabase, use the **Session pooler** connection string (the direct connection can fail on networks without IPv6).
- Special characters in the password (`@`, `#`, `/`, `:`, `%`) must be URL-encoded, otherwise the URL is parsed incorrectly. A letters-and-numbers password avoids the problem.
- A `DATABASE_URL` exported in your shell takes priority over `.env`. If you connect to the wrong database, run `unset DATABASE_URL`.

Never commit `.env`. It is listed in `.gitignore`.

### 3. Set up the database

```bash
alembic upgrade head
```

This enables the `vector` extension, creates the tables (`users`, `task_sources`, `tasks`) and turns on row-level security so Supabase's public REST API cannot read them. The backend connects as the database owner and is not affected.

### 4. Create a development user

Authentication is not built yet, so every request currently runs as a seeded development user. Run this once in your database (for Supabase, in the SQL Editor):

```sql
INSERT INTO users (user_id, email, username, password_hash)
VALUES (gen_random_uuid(), 'dev@example.com', 'dev', 'not-a-real-hash');
```

The placeholder hash can never be used to log in. This stand-in is temporary and is replaced when real authentication is added.

### 5. Run the API

```bash
uvicorn main:app --reload
```

Open http://127.0.0.1:8000/docs for the interactive Swagger UI.

## API

### Conventions

- Base path: `/api/v1`
- IDs are UUIDs, timestamps are ISO 8601 in UTC, JSON fields are `snake_case`
- Success responses wrap the payload: `{"data": ...}`
- Error responses look like `{"error": {"message": "..."}}`
- Status codes: `200` OK, `201` created, `404` not found, `409` conflict, `422` validation error, `502` upstream AI service failed

### Endpoints

| Method | Path | Description |
|---|---|---|
| `GET` | `/system-status` | Health check |
| `POST` | `/api/v1/task-sources` | Store raw input (`text`, `email` or `voice`) to be processed later |
| `POST` | `/api/v1/task-sources/{source_id}/process` | Send the stored input to Gemini and create the tasks it extracts |

Example:

```bash
# 1. Store a dump
curl -X POST http://127.0.0.1:8000/api/v1/task-sources \
  -H "Content-Type: application/json" \
  -d '{"input_type": "text", "raw_input": "buy milk, call mum tonight, finish the report by Friday"}'

# 2. Process it (use the source_id from step 1)
curl -X POST http://127.0.0.1:8000/api/v1/task-sources/<source_id>/process
```

A source can only be processed once. Processing it again returns `409`.

## Database migrations

Schema changes go through Alembic, so the history lives in git.

```bash
# after changing a model in app/models/
alembic revision --autogenerate -m "describe the change"
# read the generated file in alembic/versions/ before applying it
alembic upgrade head
```

- Every new model must be imported in `app/models/__init__.py`, otherwise autogenerate cannot see it.
- Enable row-level security in the same migration that creates a new table.
- Alembic does not drop enum types on downgrade, so add `DROP TYPE` statements to `downgrade()` when a migration creates enums.

## Testing and code quality

```bash
pytest                       # run the tests
ruff check --fix .           # lint and auto-fix (also sorts imports)
ruff format .                # format
```

Before committing, this should pass:

```bash
ruff check . && ruff format --check . && pytest
```
