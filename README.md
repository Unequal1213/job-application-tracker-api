# Job Application Tracker API

[![CI](https://github.com/Unequal1213/job-application-tracker-api/actions/workflows/ci.yml/badge.svg)](https://github.com/Unequal1213/job-application-tracker-api/actions/workflows/ci.yml)

Production-style FastAPI backend for tracking job applications, companies,
statuses, notes, sources, and simple application statistics.

This project is built as a portfolio backend API for a Junior Python Backend
Developer role. It demonstrates REST API design, relational database modeling,
service-layer business logic, validation, migrations, automated tests, Docker,
and GitHub Actions CI.

## Features

- Health check endpoint for service monitoring.
- Company CRUD endpoints.
- Job application CRUD endpoints linked to company records.
- Application filtering by status, company, and source.
- Pagination with `limit` and `offset`.
- Sorting by application fields such as `created_at`, `status`, and `source`.
- Application statistics endpoint with counts by status.
- PostgreSQL database support with SQLAlchemy.
- Alembic migrations for database schema management.
- Docker Compose setup for the API and PostgreSQL.
- Pytest test suite using an in-memory SQLite database.
- Ruff linting.
- GitHub Actions CI for every push and pull request.

## Tech Stack

- Python 3.13
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Pydantic
- Docker and Docker Compose
- Pytest
- Ruff
- GitHub Actions

## Project Structure

```text
app/
  api/          FastAPI route handlers
  database/     Database engine, session, and Base setup
  models/       SQLAlchemy models
  schemas/      Pydantic request and response schemas
  services/     Business logic and database queries
  main.py       FastAPI app entry point
alembic/
  versions/     Database migration files
tests/          Pytest test suite
.github/
  workflows/    GitHub Actions CI workflow
```

Route handlers are intentionally thin. Most database and business logic lives in
`app/services/`, which keeps the code easier to test and maintain.

## Environment Variables

Create a local `.env` file from the example file:

```bash
cp .env.example .env
```

The project expects these variables:

```text
POSTGRES_USER=job_tracker_user
POSTGRES_PASSWORD=change_me
POSTGRES_DB=job_tracker_db
DATABASE_URL=postgresql+psycopg://job_tracker_user:change_me@postgres:5432/job_tracker_db
```

Use placeholder values for local development only. Do not commit real secrets or
production credentials.

## Docker Setup

Build and start the API with PostgreSQL:

```bash
docker compose up --build
```

The app container runs Alembic migrations automatically before starting Uvicorn.

The API will be available at:

```text
http://localhost:8000
```

Check that the app is running:

```bash
curl http://localhost:8000/health
```

Expected response:

```json
{"status":"ok"}
```

Stop the containers:

```bash
docker compose down
```

To remove the PostgreSQL volume as well:

```bash
docker compose down -v
```

## Local Development Setup

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install development dependencies:

```bash
python -m pip install -r requirements-dev.txt
```

Create `.env` from `.env.example` and adjust values for your local database:

```bash
cp .env.example .env
```

Run the app locally:

```bash
uvicorn app.main:app --reload
```

If running outside Docker, make sure `DATABASE_URL` points to a reachable
PostgreSQL database.

## Database Migrations

Apply migrations:

```bash
alembic upgrade head
```

Create a new migration after model changes:

```bash
alembic revision --autogenerate -m "describe change"
```

Check the current migration version:

```bash
alembic current
```

## Tests

Run the test suite:

```bash
python -m pytest
```

Tests use an in-memory SQLite database and FastAPI dependency overrides, so they
do not require a real PostgreSQL database.

## Linting

Run Ruff:

```bash
python -m ruff check .
```

## API Endpoints

### Health

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/health` | Check that the API is running |

### Companies

| Method | Endpoint | Description |
| --- | --- | --- |
| POST | `/companies` | Create a company |
| GET | `/companies` | List companies |
| GET | `/companies/{company_id}` | Get one company |
| PATCH | `/companies/{company_id}` | Partially update a company |
| DELETE | `/companies/{company_id}` | Delete a company |

### Job Applications

| Method | Endpoint | Description |
| --- | --- | --- |
| POST | `/applications` | Create a job application |
| GET | `/applications` | List job applications |
| GET | `/applications/{application_id}` | Get one job application |
| PATCH | `/applications/{application_id}` | Partially update a job application |
| DELETE | `/applications/{application_id}` | Delete a job application |
| GET | `/applications/stats` | Get application statistics |

`GET /applications` supports these query parameters:

- `limit`: default `20`, minimum `1`, maximum `100`
- `offset`: default `0`, minimum `0`
- `status`: one of `saved`, `applied`, `interview`, `rejected`, `offer`
- `company_id`: filter by company
- `source`: filter by application source
- `sort_by`: one of `applied_at`, `created_at`, `updated_at`, `position_title`, `status`, `source`
- `sort_order`: `asc` or `desc`

Default sorting is `created_at desc`.

## Application Statistics

`GET /applications/stats` returns counts for all applications:

```json
{
  "total": 6,
  "saved": 1,
  "applied": 2,
  "interview": 1,
  "rejected": 1,
  "offer": 1
}
```

If there are no applications, all counts return `0`. This endpoint is useful for
showing a quick overview of the job search pipeline.

## Continuous Integration

GitHub Actions runs on every push and pull request.

The CI workflow:

- uses Python 3.13
- installs `requirements-dev.txt`
- runs `python -m ruff check .`
- runs `python -m pytest`

This helps keep the project linted and tested before changes are merged.
