from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

ApplicationStatus = Literal["saved", "applied", "interview", "rejected", "offer"]
ApplicationSortBy = Literal[
    "applied_at",
    "created_at",
    "updated_at",
    "position_title",
    "status",
    "source",
]
ApplicationSortOrder = Literal["asc", "desc"]


class JobApplicationCreate(BaseModel):
    company_id: int = Field(gt=0)
    position_title: str = Field(min_length=1, max_length=255)
    job_url: str | None = Field(default=None, max_length=1000)
    status: ApplicationStatus = "saved"
    source: str | None = Field(default=None, max_length=100)
    notes: str | None = None
    applied_at: datetime | None = None


class JobApplicationUpdate(BaseModel):
    company_id: int | None = Field(default=None, gt=0)
    position_title: str | None = Field(default=None, min_length=1, max_length=255)
    job_url: str | None = Field(default=None, max_length=1000)
    status: ApplicationStatus | None = None
    source: str | None = Field(default=None, max_length=100)
    notes: str | None = None
    applied_at: datetime | None = None

    @field_validator("company_id", "position_title", "status")
    @classmethod
    def validate_required_fields(cls, value: object | None) -> object:
        if value is None:
            raise ValueError("Field cannot be null.")
        return value


class JobApplicationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    company_id: int
    position_title: str
    job_url: str | None
    status: str
    source: str | None
    notes: str | None
    applied_at: datetime | None
    created_at: datetime
    updated_at: datetime
