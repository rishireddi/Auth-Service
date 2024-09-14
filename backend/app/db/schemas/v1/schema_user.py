# Built-in Dependencies
from typing import Annotated
from datetime import datetime

# Third-Party Dependencies
from pydantic import BaseModel, Field, ConfigDict

# Local Dependencies
from app.db.models.common import UUIDMixin, TimestampMixin, SoftDeleteMixin
from app.utils.partial import optional
from app.db.models.user import (
    UserInfoBase, 
    UserSecurityBase, 
    UserRoleBase
    )
from app.db.models.common import Base

class UserBase(UserInfoBase):
    pass


class User(
    UserBase,
    UUIDMixin,
    TimestampMixin,
    SoftDeleteMixin,
):
    pass


class UserRead(
    UserBase,
    UserRoleBase,
    UUIDMixin,
):
    pass


class UserCreate(
    UserBase,
    UserRoleBase
):
    model_config = ConfigDict(extra="forbid")
    password: Annotated[
        str,
        Field(
            default="P@ssword12",
            pattern=r"^.{8,}|[0-9]+|[A-Z]+|[a-z]+|[^a-zA-Z0-9]+$",
            examples=["Str1ngst!"],
        ),
    ]


class UserCreateInternal(
    UserBase,
    UserRoleBase,
    UserSecurityBase,
):
    pass


@optional()
class UserUpdate(
    UserBase,
    UserRoleBase
):
    model_config = ConfigDict(extra="forbid")


class UserUpdateInternal(UserUpdate):
    updated_at: datetime

class UserPasswordReset(Base):
    current_password: str
    new_password: str

class UserDelete(SoftDeleteMixin):
    model_config = ConfigDict(extra="forbid")


class UserRestoreDeleted(BaseModel):
    is_deleted: bool
