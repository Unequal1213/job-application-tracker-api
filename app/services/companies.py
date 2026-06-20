from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.company import Company
from app.schemas.company import CompanyCreate, CompanyUpdate


def create_company(db: Session, company_data: CompanyCreate) -> Company:
    company = Company(**company_data.model_dump())
    db.add(company)
    db.commit()
    db.refresh(company)
    return company


def list_companies(db: Session) -> list[Company]:
    return list(db.scalars(select(Company).order_by(Company.id)).all())


def get_company(db: Session, company_id: int) -> Company | None:
    return db.get(Company, company_id)


def update_company(
    db: Session,
    company: Company,
    company_data: CompanyUpdate,
) -> Company:
    update_data = company_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(company, field, value)

    db.commit()
    db.refresh(company)
    return company


def delete_company(db: Session, company: Company) -> None:
    db.delete(company)
    db.commit()
