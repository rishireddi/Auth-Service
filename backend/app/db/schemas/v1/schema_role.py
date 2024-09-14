# Built-in Dependencies
from typing import Annotated
from datetime import datetime

# Third-Party Dependencies
from pydantic import BaseModel, Field, ConfigDict

# Local Dependencies
from app.db.models.common import UUIDMixin, TimestampMixin, SoftDeleteMixin
from app.utils.partial import optional
from app.db.models.role import RoleInfoBase
from app.db.models.common import Base

class RoleBase(RoleInfoBase):
    pass


class Role(
    RoleBase,
    UUIDMixin,
    TimestampMixin,
    SoftDeleteMixin,
):
    pass


class RoleRead(
    RoleBase,
    UUIDMixin,
):
    pass


class RoleCreate(RoleBase):
    model_config = ConfigDict(extra="forbid")
    password: Annotated[
        str,
        Field(
            default="P@ssword12",
            pattern=r"^.{8,}|[0-9]+|[A-Z]+|[a-z]+|[^a-zA-Z0-9]+$",
            examples=["Str1ngst!"],
        ),
    ]


class RoleCreateInternal(
    RoleBase,
):
    pass


@optional()
class RoleUpdate(RoleBase):
    model_config = ConfigDict(extra="forbid")


class RoleUpdateInternal(RoleUpdate):
    updated_at: datetime

class RoleDelete(SoftDeleteMixin):
    model_config = ConfigDict(extra="forbid")


class RoleRestoreDeleted(BaseModel):
    is_deleted: bool
