from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.job_application import JobApplication
from app.schemas.job_application import (
    ApplicationSortBy,
    ApplicationSortOrder,
    ApplicationStatus,
    JobApplicationCreate,
    JobApplicationResponse,
    JobApplicationStatsResponse,
    JobApplicationUpdate,
)
from app.services import job_applications as application_service

router = APIRouter(prefix="/applications", tags=["applications"])

DbSession = Annotated[Session, Depends(get_db)]
ApplicationLimit = Annotated[int, Query(ge=1, le=100)]
ApplicationOffset = Annotated[int, Query(ge=0)]
ApplicationStatusFilter = Annotated[ApplicationStatus | None, Query(alias="status")]
ApplicationCompanyFilter = Annotated[int | None, Query(gt=0)]


@router.post(
    "",
    response_model=JobApplicationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_application(
    application_data: JobApplicationCreate,
    db: DbSession,
) -> JobApplication:
    application = application_service.create_application(db, application_data)
    if application is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found",
        )

    return application


@router.get("", response_model=list[JobApplicationResponse])
def list_applications(
    db: DbSession,
    limit: ApplicationLimit = 20,
    offset: ApplicationOffset = 0,
    status_filter: ApplicationStatusFilter = None,
    company_id: ApplicationCompanyFilter = None,
    source: str | None = None,
    sort_by: ApplicationSortBy = "created_at",
    sort_order: ApplicationSortOrder = "desc",
) -> list[JobApplication]:
    return application_service.list_applications(
        db,
        limit=limit,
        offset=offset,
        status=status_filter,
        company_id=company_id,
        source=source,
        sort_by=sort_by,
        sort_order=sort_order,
    )


@router.get("/stats", response_model=JobApplicationStatsResponse)
def get_application_stats(db: DbSession) -> JobApplicationStatsResponse:
    return application_service.get_application_stats(db)


@router.get("/{application_id}", response_model=JobApplicationResponse)
def get_application(application_id: int, db: DbSession) -> JobApplication:
    application = application_service.get_application(db, application_id)
    if application is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found",
        )

    return application


@router.patch("/{application_id}", response_model=JobApplicationResponse)
def update_application(
    application_id: int,
    application_data: JobApplicationUpdate,
    db: DbSession,
) -> JobApplication:
    application = application_service.get_application(db, application_id)
    if application is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found",
        )

    updated_application = application_service.update_application(
        db,
        application,
        application_data,
    )
    if updated_application is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found",
        )

    return updated_application


@router.delete("/{application_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_application(application_id: int, db: DbSession) -> Response:
    application = application_service.get_application(db, application_id)
    if application is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found",
        )

    application_service.delete_application(db, application)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
