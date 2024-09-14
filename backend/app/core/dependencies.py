# Built-in Dependencies
from typing import Annotated, Union, Any, Dict
import logging
import os

# Third-Party Dependencies
from fastapi import Depends, HTTPException, Request
from sqlmodel.ext.asyncio.session import AsyncSession

# Local Dependencies
from app.db.crud.crud_user import crud_users
from app.core.http_exceptions import (
    UnauthorizedException,
    ForbiddenException,
    # RateLimitException
)

from app.db.session import async_get_db
from app.core.security import oauth2_scheme, verify_token
from app.db.schemas.v1.schema_user import UserRead
from app.db.crud.crud_role import crud_role, get_role
from app.db.schemas.v1.schema_role import RoleCreate

# Logger instance
logger = logging.getLogger(__name__)


# Function to get the current user based on the provided authentication token
async def get_current_user(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(async_get_db)
) -> Union[Dict[str, Any], None]:

    credentials_exception = UnauthorizedException("User not authenticated.")

    token_data = await verify_token(token, db)
    if token_data is None:
        raise credentials_exception

    # Check if the authentication token represents an email or username and retrieve the user information
    if "@" in token_data.email:
        user: dict = await crud_users.get(
            db=db, email=token_data.email, is_deleted=False
        )
    else:
        user = await crud_users.get(
            db=db, username=token_data.email, is_deleted=False
        )

    if user:
        # Return the user information if available
        return user

    # Raise an exception if the user is not authenticated
    raise credentials_exception


async def ensure_owner_role(db: AsyncSession, org_id: str) -> Dict[str, Any]:
    # Check if "owner" role exists
    existing_role = await get_role(db=db, role_name="owner", org_id=org_id)
    
    if not existing_role:
        # Create the "owner" role if it doesn't exist
        role_data = RoleCreate(name="owner", description="Organization owner role", org_id=org_id)
        new_role = await crud_role.create(db=db, obj_in=role_data)
        logger.info(f"'Owner' role created successfully for organization {org_id}")
        return new_role
    
    logger.info(f"'Owner' role already exists for organization {org_id}")
    return existing_role

async def get_current_owner(
    current_user: Annotated[dict, Depends(get_current_user)], db: AsyncSession = Depends(async_get_db)
) -> dict:
    # Ensure that the "owner" role exists
    owner_role = await ensure_owner_role(db=db, org_id=current_user['org_id'])

    # Check if the user has the "owner" role
    if owner_role and current_user.get("role") == "owner":
        return current_user

    raise ForbiddenException("You do not have owner privileges.")

def create_folders(root_folder, sub_folders):
    # Create the root folder if it doesn't exist
    if not os.path.exists(root_folder):
        os.makedirs(root_folder)

    # Create sub_folders inside the root folder
    for subfolder in sub_folders:
        subfolder_path = os.path.join(root_folder, subfolder)
        if not os.path.exists(subfolder_path):
            os.makedirs(subfolder_path)


CurrentUser = Annotated[UserRead, Depends(get_current_user)]
CurrentSuperUser = Annotated[UserRead, Depends(get_current_user)]