# Built-in Dependencies
from uuid import UUID
from typing import Optional

# Third-Party Dependencies
from sqlmodel import Field, Column, JSON

# Local Dependencies
from app.db.models.common import (
    UUIDMixin,
    TimestampMixin,
    SoftDeleteMixin,
    Base,
)

from app.core.config import settings


class OrganizationInfoBase(Base):
    organizationName: str = Field(nullable=False)
    organizationStatus: int = Field(default=0, nullable=False)
    organizationPersonal: Optional[bool] = False
    organizationSettings: Optional[dict] = Field(default=None, sa_column=Column(JSON, nullable=True))

class Organization(
    OrganizationInfoBase,
    UUIDMixin,
    TimestampMixin,
    SoftDeleteMixin,
    table=True,
):
    __tablename__ = f"{settings.DATABASE_ORGANIZATION_TABLE}"