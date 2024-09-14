# Built-in Dependencies
from datetime import datetime

# Third-Party Dependencies
from pydantic import Field

# Local Dependencies
from app.db.models.common import TimestampMixin, UUIDMixin, Base


class LoginInput(Base):
    email: str = Field(unique=True, nullable=False)
    password: str

class TokenBlacklistBase(Base):
    # Data Columns
    token: str = Field(
        index=True,
        nullable=False,
        default=None,
        description="Token value for authentication",
    )
    expires_at: datetime = Field(
        nullable=False,
        default=None,
        description="Timestamp indicating the expiration date and time of the token",
    )


class TokenBlacklist(TokenBlacklistBase, UUIDMixin, TimestampMixin, table=True):
    __tablename__ = "system_token_blacklist"
