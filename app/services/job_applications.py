from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.company import Company
from app.models.job_application import JobApplication
from app.schemas.job_application import (
    ApplicationSortBy,
    ApplicationSortOrder,
    ApplicationStatus,
    JobApplicationCreate,
    JobApplicationUpdate,
)

APPLICATION_STATUSES: tuple[ApplicationStatus, ...] = (
    "saved",
    "applied",
    "interview",
    "rejected",
    "offer",
)


def create_application(
    db: Session,
    application_data: JobApplicationCreate,
) -> JobApplication | None:
    if db.get(Company, application_data.company_id) is None:
        return None

    application = JobApplication(**application_data.model_dump())
    db.add(application)
    db.commit()
    db.refresh(application)
    return application


def list_applications(
    db: Session,
    *,
    limit: int = 20,
    offset: int = 0,
    status: ApplicationStatus | None = None,
    company_id: int | None = None,
    source: str | None = None,
    sort_by: ApplicationSortBy = "created_at",
    sort_order: ApplicationSortOrder = "desc",
) -> list[JobApplication]:
    statement = select(JobApplication)

    if status is not None:
        statement = statement.where(JobApplication.status == status)
    if company_id is not None:
        statement = statement.where(JobApplication.company_id == company_id)
    if source is not None:
        statement = statement.where(JobApplication.source == source)

    sort_column = getattr(JobApplication, sort_by)
    if sort_order == "desc":
        sort_column = sort_column.desc()
    else:
        sort_column = sort_column.asc()

    statement = statement.order_by(sort_column).offset(offset).limit(limit)
    return list(db.scalars(statement).all())


def get_application(db: Session, application_id: int) -> JobApplication | None:
    return db.get(JobApplication, application_id)


def get_application_stats(db: Session) -> dict[str, int]:
    counts = dict.fromkeys(APPLICATION_STATUSES, 0)
    rows = db.execute(
        select(JobApplication.status, func.count()).group_by(JobApplication.status)
    ).all()

    total = 0
    for application_status, count in rows:
        counts[application_status] = count
        total += count

    return {"total": total, **counts}


def update_application(
    db: Session,
    application: JobApplication,
    application_data: JobApplicationUpdate,
) -> JobApplication | None:
    update_data = application_data.model_dump(exclude_unset=True)

    company_id = update_data.get("company_id")
    if company_id is not None and db.get(Company, company_id) is None:
        return None

    for field, value in update_data.items():
        setattr(application, field, value)

    db.commit()
    db.refresh(application)
    return application


def delete_application(db: Session, application: JobApplication) -> None:
    db.delete(application)
    db.commit()
