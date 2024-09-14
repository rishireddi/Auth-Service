from pydantic import BaseModel

# Local Dependencies
from app.db.models.auth import TokenBlacklistBase
from app.utils.partial import optional
from app.db.models.user import UserInfoBase, UserRoleBase
from app.db.models.organization import OrganizationInfoBase
from typing import Annotated

# Third-Party Dependencies
from pydantic import BaseModel, Field, ConfigDict

# class SignUpRead(SignUpInput):
#     pass

class SignUpCreate(
    UserInfoBase,
    UserRoleBase,
    OrganizationInfoBase,
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
    memberName: str
    memberStatus: int = Field(default=0, nullable=False)

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str


class TokenBlacklistCreate(TokenBlacklistBase):
    pass


# All these fields are optional
@optional()
class TokenBlacklistUpdate(TokenBlacklistBase):
    pass
