# Built-in Dependencies
from typing import Annotated, Dict
from datetime import timedelta

# Third-party Dependencies
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError
from fastapi import Response, Request, Depends, APIRouter
from sqlmodel.ext.asyncio.session import AsyncSession


# Local Dependencies
from app.core.http_exceptions import UnauthorizedException
from app.core.config import settings
from app.db.schemas.v1.schema_auth import Token
from app.db.session import async_get_db
from app.core.security import (
    create_access_token,
    authenticate_user,
    create_refresh_token,
    verify_token,
    oauth2_scheme,
    blacklist_token,
)
from app.db.crud.crud_user import crud_users
from app.core.hashing import Hasher
from app.core.dependencies import CurrentUser
from app.db.schemas.v1.schema_user import UserPasswordReset
from app.db.models.auth import LoginInput


router = APIRouter(tags=["Login"])


@router.post("/login", response_model=Token)
async def login_for_access_token(
    response: Response,
    form_data: LoginInput,
    db: Annotated[AsyncSession, Depends(async_get_db)],
) -> Dict[str, str]:
    user = await authenticate_user(
        email_or_password=form_data.email, password=form_data.password, db=db
    )
    if not user:
        raise UnauthorizedException("Wrong email or password.")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await create_access_token(
        data={"sub": user["email"]}, expires_delta=access_token_expires
    )

    refresh_token = await create_refresh_token(data={"sub": user["email"]})
    max_age = settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=settings.COOKIES_SECURE_SETTINGS,
        samesite="Lax",
        max_age=max_age,
    )
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        secure=settings.COOKIES_SECURE_SETTINGS,
        samesite="Lax",
        max_age=max_age,
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/refresh")
async def refresh_access_token(
    request: Request, db: AsyncSession = Depends(async_get_db)
) -> Dict[str, str]:
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise UnauthorizedException("Refresh token missing.")

    user_data = await verify_token(refresh_token, db)
    if not user_data:
        raise UnauthorizedException("Invalid refresh token.")

    new_access_token = await create_access_token(
        data={"sub": user_data.username_or_email}
    )
    return {"access_token": new_access_token, "token_type": "bearer"}


@router.post("/logout")
async def logout(
    response: Response,
    access_token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(async_get_db),
) -> Dict[str, str]:
    try:
        await blacklist_token(token=access_token, db=db)
        response.delete_cookie(key="access_token")
        response.delete_cookie(key="refresh_token")

        return {"message": "Logged out successfully"}

    except JWTError:
        raise UnauthorizedException("Invalid token.")

@router.post("/change-password")
async def change_password(
    password_change: UserPasswordReset,
    current_user: CurrentUser,
    db: AsyncSession = Depends(async_get_db),
):
    db_user = await crud_users.get(db=db, email=current_user["email"])
    
    if not db_user:
        raise UnauthorizedException("User not found.")
    
    if not Hasher.verify_password(password_change.current_password, db_user["hashed_password"]):
        raise UnauthorizedException("Current password is incorrect.")
    
    hashed_new_password = Hasher.get_hash_password(password_change.new_password)
    
    await crud_users.update(db=db, id=db_user["id"], object={"hashed_password": hashed_new_password})
    
    return {"message": "Password changed successfully."}