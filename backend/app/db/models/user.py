# Built-in Dependencies
from uuid import UUID
from typing import Optional

# Third-Party Dependencies
from sqlmodel import Field, Column, JSON
from enum import IntEnum

# Local Dependencies
from app.db.models.common import (
    UUIDMixin,
    TimestampMixin,
    SoftDeleteMixin,
    Base,
)

from app.core.config import settings
from pydantic import validator


class UserInfoBase(Base):
    email: str = Field(unique=True, nullable=False)
    userProfile: dict = Field(default={}, sa_column=Column(JSON, nullable=False))
    userStatus: int = Field(default=0, nullable=False)
    userSettings: Optional[dict] = Field(default=None, sa_column=Column(JSON, nullable=True))

class UserSecurityBase(Base):
    hashed_password: str = Field(
        nullable=False, description="Hashed password for user authentication"
    )

class AccessLevelBase(IntEnum):
    GUEST_USER: int                 = 0
    DESIGN_ENGINEER: int            = 5
    TESTING_ENGINEER: int           = 10
    SOFTWARE_DEVELOPER: int         = 20
    MANAGER: int                    = 30
    TEAM_LEAD: int                  = 40
    COMPANY_ADMIN: int              = 60
    OWNER: int                      = 100


class UserRoleBase(Base):
    user_role: int = Field(
        default=0,
        description="Role of the user in the company.",
        schema_extra={"Examples": 1},  # Adjust examples as needed
    )

    # validation of both str and int for user_role
    @validator("user_role", pre=True, always=True)
    def validate_user_role(cls, value):
        if isinstance(value, str):
            try:
                return AccessLevelBase[value.upper()]
            except KeyError:
                raise ValueError(f"Invalid user role: {value}")
        elif isinstance(value, int):
            return AccessLevelBase(value)
        else:
            raise ValueError("User role must be a string or an integer")
class User(
    UserInfoBase,
    UserRoleBase,
    UserSecurityBase,
    UUIDMixin,
    TimestampMixin,
    SoftDeleteMixin,
    table=True,
):
    __tablename__ = f"{settings.DATABASE_USER_TABLE}"
