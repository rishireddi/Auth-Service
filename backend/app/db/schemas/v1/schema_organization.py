# Built-in Dependencies
from typing import Annotated
from datetime import datetime

# Third-Party Dependencies
from pydantic import BaseModel, Field, ConfigDict

# Local Dependencies
from app.db.models.common import UUIDMixin, TimestampMixin, SoftDeleteMixin
from app.utils.partial import optional
from app.db.models.organization import OrganizationInfoBase
from app.db.models.common import Base

class OrganizationBase(OrganizationInfoBase):
    pass


class Organization(
    OrganizationBase,
    UUIDMixin,
    TimestampMixin,
    SoftDeleteMixin,
):
    pass


class OrganizationRead(
    OrganizationBase,
    UUIDMixin,
):
    pass


class OrganizationCreate(OrganizationBase):
    model_config = ConfigDict(extra="forbid")
    password: Annotated[
        str,
        Field(
            default="P@ssword12",
            pattern=r"^.{8,}|[0-9]+|[A-Z]+|[a-z]+|[^a-zA-Z0-9]+$",
            examples=["Str1ngst!"],
        ),
    ]


class OrganizationCreateInternal(
    OrganizationBase,
):
    pass


@optional()
class OrganizationUpdate(OrganizationBase):
    model_config = ConfigDict(extra="forbid")


class OrganizationUpdateInternal(OrganizationUpdate):
    updated_at: datetime

class OrganizationDelete(SoftDeleteMixin):
    model_config = ConfigDict(extra="forbid")


class OrganizationRestoreDeleted(BaseModel):
    is_deleted: bool
