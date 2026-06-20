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

## API

Health:

- `GET /health`

Companies:

- `POST /companies`
- `GET /companies`
- `GET /companies/{company_id}`
- `PATCH /companies/{company_id}`
- `DELETE /companies/{company_id}`

Applications:

- `POST /applications`
- `GET /applications`
- `GET /applications/{application_id}`
- `PATCH /applications/{application_id}`
- `DELETE /applications/{application_id}`
