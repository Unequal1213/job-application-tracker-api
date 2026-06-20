from fastapi import FastAPI

from app.api.applications import router as applications_router
from app.api.companies import router as companies_router
from app.api.health import router as health_router

app = FastAPI(title="Job Application Tracker API")

app.include_router(health_router)
app.include_router(companies_router)
app.include_router(applications_router)
