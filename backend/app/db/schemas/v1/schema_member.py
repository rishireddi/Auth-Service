# Built-in Dependencies
from typing import Annotated
from datetime import datetime

# Third-Party Dependencies
from pydantic import BaseModel, Field, ConfigDict

# Local Dependencies
from app.db.models.common import UUIDMixin, TimestampMixin, SoftDeleteMixin
from app.utils.partial import optional
from app.db.models.member import MemberInfoBase
from app.db.models.common import Base

class MemberBase(MemberInfoBase):
    pass


class Member(
    MemberBase,
    UUIDMixin,
    TimestampMixin,
    SoftDeleteMixin,
):
    pass


class MemberRead(
    MemberBase,
    UUIDMixin,
):
    pass


class MemberCreate(MemberBase):
    model_config = ConfigDict(extra="forbid")


class MemberCreateInternal(
    MemberBase,
):
    pass


@optional()
class MemberUpdate(MemberBase):
    model_config = ConfigDict(extra="forbid")


class MemberUpdateInternal(MemberUpdate):
    updated_at: datetime

class MemberDelete(SoftDeleteMixin):
    model_config = ConfigDict(extra="forbid")


class MemberRestoreDeleted(BaseModel):
    is_deleted: bool
