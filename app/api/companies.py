from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.company import Company
from app.schemas.company import CompanyCreate, CompanyResponse, CompanyUpdate
from app.services import companies as company_service

router = APIRouter(prefix="/companies", tags=["companies"])

DbSession = Annotated[Session, Depends(get_db)]


@router.post("", response_model=CompanyResponse, status_code=status.HTTP_201_CREATED)
def create_company(company_data: CompanyCreate, db: DbSession) -> Company:
    return company_service.create_company(db, company_data)


@router.get("", response_model=list[CompanyResponse])
def list_companies(db: DbSession) -> list[Company]:
    return company_service.list_companies(db)


@router.get("/{company_id}", response_model=CompanyResponse)
def get_company(company_id: int, db: DbSession) -> Company:
    company = company_service.get_company(db, company_id)
    if company is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found",
        )

    return company


@router.patch("/{company_id}", response_model=CompanyResponse)
def update_company(
    company_id: int,
    company_data: CompanyUpdate,
    db: DbSession,
) -> Company:
    company = company_service.get_company(db, company_id)
    if company is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found",
        )

    return company_service.update_company(db, company, company_data)


@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_company(company_id: int, db: DbSession) -> Response:
    company = company_service.get_company(db, company_id)
    if company is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found",
        )

    company_service.delete_company(db, company)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
