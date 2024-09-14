# Built-in Dependencies
from uuid import UUID

# Third-Party Dependencies
from sqlmodel import Field

# Local Dependencies
from app.db.models.common import (
    UUIDMixin,
    TimestampMixin,
    SoftDeleteMixin,
    Base,
)

from app.core.config import settings


class RoleInfoBase(Base):
    roleName: str = Field(nullable=False)
    roleDescription: str = Field(nullable=True)
    org_id: UUID = Field(
        foreign_key=f"{settings.DATABASE_ORGANIZATION_TABLE}.id",
        nullable=False
    )

class Role(
    RoleInfoBase,
    UUIDMixin,
    TimestampMixin,
    SoftDeleteMixin,
    table=True,
):
    __tablename__ = f"{settings.DATABASE_ROLE_TABLE}"