# Job Application Tracker API

FastAPI backend for tracking job applications.

## Run With Docker

Create a local `.env` file from the example values:

```bash
cp .env.example .env
```

Start the API and PostgreSQL:

```bash
docker compose up --build
```

The app service runs Alembic migrations before starting Uvicorn.

Health check:

```bash
curl http://localhost:8000/health
```

Expected response:

```json
{"status":"ok"}
```
