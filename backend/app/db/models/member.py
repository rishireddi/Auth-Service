# Built-in Dependencies
from uuid import UUID
from typing import Optional

# Third-Party Dependencies
from sqlmodel import Field, Column, JSON
from pydantic import EmailStr

# Local Dependencies
from app.db.models.common import (
    UUIDMixin,
    TimestampMixin,
    SoftDeleteMixin,
    Base,
)

from app.core.config import settings

class MemberInfoBase(Base):
    org_id: UUID = Field(
        foreign_key=f"{settings.DATABASE_ORGANIZATION_TABLE}.id",
        nullable=False
    )
    user_id: UUID = Field(
        foreign_key=f"{settings.DATABASE_USER_TABLE}.id", 
        nullable=False
    )
    role_id: UUID = Field(
        foreign_key=f"{settings.DATABASE_ROLE_TABLE}.id",
        nullable=False
    )
    memberStatus: int = Field(default=0, nullable=False)
    memberSettings: Optional[dict] = Field(default=None, sa_column=Column(JSON, nullable=True))
    memberName: str

class Member(
    MemberInfoBase,
    UUIDMixin,
    TimestampMixin,
    SoftDeleteMixin,
    table=True,
):
    __tablename__ = f"{settings.DATABASE_MEMBER_TABLE}"