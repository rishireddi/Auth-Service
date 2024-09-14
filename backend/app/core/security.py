from typing import Optional, Dict, Literal, Union, Any
from datetime import datetime, timedelta, timezone


# Third-Party Dependencies
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.security import OAuth2
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi import Request, HTTPException, status, Depends
from fastapi.security.utils import get_authorization_scheme_param
from jose import jwt, JWTError


# Local Dependencies
from app.core.config import settings
from app.db.schemas.v1.schema_auth import TokenData, TokenBlacklistCreate
from app.db.crud.crud_auth import crud_token_blacklist
from app.db.crud.crud_user import crud_users, get_user
from app.core.hashing import Hasher
from app.db.session import async_get_db


class OAuth2PasswordBearerWithCookie(OAuth2):
    def __init__(
        self,
        tokenUrl: str,
        scheme_name: Optional[str] = None,
        scopes: Optional[Dict[str, str]] = None,
        description: Optional[str] = None,
        auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(password={"tokenUrl": tokenUrl, "scopes": scopes})
        super().__init__(
            flows=flows,
            scheme_name=scheme_name,
            description=description,
            auto_error=auto_error,
        )

    async def __call__(self, request: Request) -> Optional[str]:
        authorization: str = request.cookies.get("access_token")
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None
        return param


oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="/auth/login")


# Function to authenticate a user based on provided credentials
async def authenticate_user(
    email_or_password: str, password: str, db: AsyncSession
) -> Union[Dict[str, Any], Literal[False]]:
    db_user = await get_user(email_or_password, db)

    if not db_user:
        return False

    elif not Hasher.verify_password(password, db_user["hashed_password"]):
        return False

    return db_user


async def create_access_token(
    data: dict, expires_delta: Optional[timedelta] = None
) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


# Function to create a refresh token with optional expiration time
async def create_refresh_token(
    data: Dict[str, Any], expires_delta: timedelta = None
) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc).replace(tzinfo=None) + expires_delta
    else:
        expire = datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS
        )
    to_encode.update({"exp": expire})
    encoded_jwt: str = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


# Function to verify the validity of a token and return TokenData if valid
async def verify_token(token: str, db: AsyncSession) -> TokenData:

    is_blacklisted = await crud_token_blacklist.exists(db, token=token)
    if is_blacklisted:
        return None

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            return None

        user = await crud_users.get(db=db, email=email, is_deleted=False)

        if user:
            return TokenData(email=email)

        # If user is not found in Redis or PostgreSQL, blacklist the token
        await blacklist_token(token=token, db=db)

        return None

    except JWTError:
        return None


# Function to blacklist a token by storing it in the database
async def blacklist_token(token: str, db: AsyncSession) -> None:
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    expires_at = datetime.fromtimestamp(payload.get("exp"))
    await crud_token_blacklist.create(
        db,
        object=TokenBlacklistCreate(**{"token": token, "expires_at": expires_at}),
    )
