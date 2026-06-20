from app.database.database import Base
from app.models import Company, JobApplication


def test_models_are_registered_with_expected_tables() -> None:
    assert Company.__tablename__ == "companies"
    assert JobApplication.__tablename__ == "job_applications"
    assert set(Base.metadata.tables) == {"companies", "job_applications"}


def test_company_model_has_expected_columns() -> None:
    assert set(Company.__table__.columns.keys()) == {
        "id",
        "name",
        "website",
        "notes",
        "created_at",
        "updated_at",
    }


def test_job_application_model_has_expected_columns() -> None:
    assert set(JobApplication.__table__.columns.keys()) == {
        "id",
        "company_id",
        "position_title",
        "job_url",
        "status",
        "source",
        "notes",
        "applied_at",
        "created_at",
        "updated_at",
    }


def test_job_application_has_company_foreign_key() -> None:
    foreign_key = next(iter(JobApplication.__table__.c.company_id.foreign_keys))

    assert foreign_key.target_fullname == "companies.id"
