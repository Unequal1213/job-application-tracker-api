# AGENTS.md

## Project context

This is a portfolio backend project for a self-taught Junior Python Backend Developer.

Project name:
Job Application Tracker API

Main goal:
Build a production-style FastAPI backend that helps track job applications, companies, statuses, notes, and application statistics.

The project should demonstrate:
- backend API design
- database modeling
- relational data
- CRUD workflows
- analytics/statistics endpoint
- testing
- Docker
- GitHub Actions CI

## Tech stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Pydantic
- Docker
- Pytest
- Ruff
- GitHub Actions

## Development rules

- Do not rewrite the entire project unless explicitly requested.
- Make small, focused changes.
- Explain every changed file.
- Preserve a clean FastAPI project structure.
- Use type hints.
- Follow PEP8.
- Avoid quick hacks.
- Do not commit secrets.
- Do not hardcode API keys, passwords, tokens, or database URLs.
- Use environment variables for configuration.
- Keep business logic separate from API routes.
- Prefer maintainable code over clever code.

## Initial MVP

Build a backend API for tracking job applications.

Core resources:
- Company
- JobApplication

Company fields:
- id
- name
- website
- notes
- created_at
- updated_at

JobApplication fields:
- id
- company_id
- position_title
- job_url
- status
- source
- notes
- applied_at
- created_at
- updated_at

Initial endpoints:
- GET /health
- POST /companies
- GET /companies
- GET /companies/{company_id}
- POST /applications
- GET /applications
- GET /applications/{application_id}
- PATCH /applications/{application_id}
- DELETE /applications/{application_id}
- GET /applications/stats

Statuses:
- saved
- applied
- interview
- rejected
- offer

## Review guidelines

- Check for security issues.
- Check for hardcoded secrets.
- Check database session handling.
- Check API validation.
- Check test coverage.
- Check whether the code is understandable for a Junior Developer.
