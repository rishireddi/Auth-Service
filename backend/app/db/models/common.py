# Built-in Dependencies
from datetime import datetime, timezone
from uuid import UUID, uuid4
from typing import Optional, Any

# Third-Party Dependencies
from sqlmodel import SQLModel, Field, DateTime
from pydantic import field_serializer


# Define a base class for declarative models with support for dataclasses
class Base(SQLModel):
    pass


class UUIDMixin(SQLModel):
    # Data Columns
    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True,
        description="Unique identifier (UUID) for the record",
    )


class TimestampMixin(SQLModel):
    # Data Columns
    created_at: datetime = Field(
        sa_type=DateTime(timezone=True),
        default_factory=lambda: datetime.now(timezone.utc),
        description="Timestamp for the creation of the record",
    )
    updated_at: datetime = Field(
        sa_type=DateTime(timezone=True),
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"onupdate": datetime.now(timezone.utc)},
        description="Timestamp for the last update of the record",
    )

    @field_serializer("created_at")
    def serialize_dt(self, created_at: datetime, _info: Any) -> str:
        if created_at is not None:
            return created_at.isoformat()

        return None

    @field_serializer("updated_at")
    def serialize_updated_at(self, updated_at: datetime, _info: Any) -> str:
        if updated_at is not None:
            return updated_at.isoformat()

        return None


class SoftDeleteMixin(SQLModel):

    # Data Columns
    deleted_at: Optional[datetime] = Field(
        sa_type=DateTime(timezone=True),
        default=None,
        description="Timestamp for the deletion of the record (soft deletion)",
    )
    is_deleted: bool = Field(
        default=False,
        index=True,
        description="Flag indicating whether the record is deleted (soft deletion)",
    )

    @field_serializer("deleted_at")
    def serialize_dates(self, deleted_at: datetime, _info: Any) -> str:
        if deleted_at is not None:
            return deleted_at.isoformat()

        return None
