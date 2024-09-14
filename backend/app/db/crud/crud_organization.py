from typing import Dict, Any, Literal, Union

# Third-Party Dependencies
from sqlmodel.ext.asyncio.session import AsyncSession

# Local Dependencies
from app.db.crud.base import CRUDBase
from app.db.models.organization import Organization
from app.db.schemas.v1.schema_organization import (
    OrganizationCreateInternal,
    OrganizationUpdate,
    OrganizationUpdateInternal,
    OrganizationDelete,
    OrganizationCreate,
    OrganizationRead
)

from app.core.http_exceptions import (
    DuplicateValueException,
    NotFoundException,
    ForbiddenException,
    # RateLimitException
)

from app.core.hashing import Hasher

CRUDOrganization = CRUDBase[
    Organization, OrganizationCreateInternal, OrganizationUpdate, OrganizationUpdateInternal, OrganizationDelete
]

crud_organization = CRUDOrganization(Organization)


async def create_new_organization(organization: OrganizationCreate, db: AsyncSession) -> OrganizationRead:
    organizationName_row = await crud_organization.exists(db=db, organizationName=organization.organizationName)
    if organizationName_row:
        raise DuplicateValueException("Organization name is already registered")

    organization_internal_dict = organization.model_dump()

    organization_internal = OrganizationCreateInternal(**organization_internal_dict)
    print(organization_internal)
    return await crud_organization.create(db=db, object=organization_internal)

async def get_organization(organizationName: str, db: AsyncSession) -> Union[Dict[str, Any], Literal[None]]:
    db_organization: dict = await crud_organization.get(
            db=db, organizationName=organizationName, is_deleted=False
    )
    if not db_organization:
        return None
    
    return db_organization