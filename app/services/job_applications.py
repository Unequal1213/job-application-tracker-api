from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.company import Company
from app.models.job_application import JobApplication
from app.schemas.job_application import JobApplicationCreate, JobApplicationUpdate


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


def list_applications(db: Session) -> list[JobApplication]:
    return list(db.scalars(select(JobApplication).order_by(JobApplication.id)).all())


def get_application(db: Session, application_id: int) -> JobApplication | None:
    return db.get(JobApplication, application_id)


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
