from typing import Dict, Any, Literal, Union

# Third-Party Dependencies
from sqlmodel.ext.asyncio.session import AsyncSession

# Local Dependencies
from app.db.crud.base import CRUDBase
from app.db.models.user import User
from app.db.schemas.v1.schema_user import (
    UserCreateInternal,
    UserUpdate,
    UserUpdateInternal,
    UserDelete,
    UserCreate,
    UserRead
)

from app.core.http_exceptions import (
    DuplicateValueException,
    NotFoundException,
    ForbiddenException,
)

from app.core.hashing import Hasher

# CRUD operations for the 'User' model
CRUDUser = CRUDBase[
    User, UserCreateInternal, UserUpdate, UserUpdateInternal, UserDelete
]

# Create an instance of CRUDUser for the 'User' model
crud_users = CRUDUser(User)


async def create_new_user(user: UserCreate, db: AsyncSession) -> UserRead:
    email_row = await crud_users.exists(db=db, email=user.email)
    if email_row:
        raise DuplicateValueException("Email is already registered")

    user_internal_dict = user.model_dump()
    user_internal_dict["hashed_password"] = Hasher.get_hash_password(
        plain_password=user_internal_dict["password"]
    )
    del user_internal_dict["password"]

    user_internal = UserCreateInternal(**user_internal_dict)
    print(user_internal)
    return await crud_users.create(db=db, object=user_internal)

async def get_user(email: str, db: AsyncSession) -> Union[Dict[str, Any], Literal[None]]:
    if "@" in email:
        db_user: dict = await crud_users.get(
            db=db, email=email, is_deleted=False
        )
        return db_user
    else:
        return None
    