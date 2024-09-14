from typing import Dict, Any, Literal, Union

# Third-Party Dependencies
from sqlmodel.ext.asyncio.session import AsyncSession

# Local Dependencies
from app.db.crud.base import CRUDBase
from app.db.models.role import Role
from app.db.schemas.v1.schema_role import (
    RoleCreateInternal,
    RoleUpdate,
    RoleUpdateInternal,
    RoleDelete,
    RoleCreate,
    RoleRead
)

from app.core.http_exceptions import (
    DuplicateValueException,
    NotFoundException,
    ForbiddenException,
    # RateLimitException
)

from app.core.hashing import Hasher

CRUDRole = CRUDBase[
    Role, RoleCreateInternal, RoleUpdate, RoleUpdateInternal, RoleDelete
]

crud_role = CRUDRole(Role)


async def create_new_role(role: RoleCreate, db: AsyncSession) -> RoleRead:
    roleName_row = await crud_role.exists(db=db, roleName=role.roleName)
    if roleName_row:
        raise DuplicateValueException("Role is already registered")

    role_internal_dict = role.model_dump()

    role_internal = RoleCreateInternal(**role_internal_dict)
    print(role_internal)
    return await crud_role.create(db=db, object=role_internal)

async def get_role(roleName: str, db: AsyncSession) -> Union[Dict[str, Any], Literal[None]]:
    db_role: dict = await crud_role.get(
            db=db, roleName=roleName, is_deleted=False
    )
    if not db_role:
        return None
    
    return db_role