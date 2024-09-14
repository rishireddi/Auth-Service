# Built-in Dependencies
from typing import Annotated, Any

# Third-Party Dependencies
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends, Request
import fastapi
from sqlalchemy import select
from sqlmodel import update

# Local Dependencies
from app.db.crud.crud_user import crud_users, create_new_user
from app.db.crud.crud_organization import crud_organization, create_new_organization
from app.db.crud.crud_role import crud_role, create_new_role, get_role
from app.db.crud.crud_member import crud_member, create_new_member
from app.db.session import async_get_db
from app.core.http_exceptions import HTTPException
from app.db.schemas.v1.schema_user import UserCreate
from app.db.schemas.v1.schema_organization import OrganizationCreate
from app.db.schemas.v1.schema_role import RoleCreate
from app.db.schemas.v1.schema_member import (
    MemberCreate,
    MemberRead,
)
from app.db.schemas.v1.schema_auth import SignUpCreate
from app.db.models.user import AccessLevelBase, User


router = fastapi.APIRouter(tags=["Users"])

@router.post("/signup", response_model=MemberRead, status_code=201)
async def signUp(
    request: Request,
    signUp_data: SignUpCreate,
    db: Annotated[AsyncSession, Depends(async_get_db)],
) -> Any:
    user_in = UserCreate(
        email=signUp_data.email,
        userProfile=signUp_data.userProfile,
        userStatus=signUp_data.userStatus,
        userSettings=signUp_data.userSettings,
        password=signUp_data.password,
        user_role=signUp_data.user_role
    )
    user = await create_new_user(user_in, db)

    # Create organization entry
    organization_in = OrganizationCreate(
        organizationName=signUp_data.organizationName,
        organizationStatus=signUp_data.organizationStatus,
        organizationPersonal=signUp_data.organizationPersonal,
        organizationSettings=signUp_data.organizationSettings,
    )

    # Create organization and associate with the user
    organization = await create_new_organization(organization_in, db)

    # Add member entry with 'owner' role
    # Ensure the 'owner' role exists or create it
    owner_role = await get_role(roleName="owner", db=db)
    
    if not owner_role:
        role_data = RoleCreate(
            roleName="owner",
            roleDescription="Owner of the Organization",
            org_id=organization.id
            )
        owner_role = await create_new_role(role_data, db)

    # Create member entry and assign 'owner' role to the user
    member_in = MemberCreate(
        user_id=user.id,
        org_id=organization.id,
        role_id=owner_role['id'],
        memberName=signUp_data.memberName,
        memberStatus=signUp_data.memberStatus
    )

    return await create_new_member(member_in, db)

@router.get("/count-by-role")
async def get_users_count_by_role(role: AccessLevelBase, db: AsyncSession = Depends(async_get_db)):
    if role not in AccessLevelBase:
        raise HTTPException(status_code=400, detail="Invalid role")
    
    result = await db.exec(select(User).where(User.user_role == role.value))
    
    users_with_role = result.all()
    user_count = len(users_with_role)
    
    return {"role": role.name, "count": user_count}

@router.patch("/change-role", status_code=200)
async def change_user_role(
    user_email: str,
    new_role: AccessLevelBase,
    db: AsyncSession = Depends(async_get_db)
):
    # Fetch the user from the database
    user_result = await db.execute(select(User).where(User.email == user_email))
    user = user_result.scalars().first()

    # If user is not found, raise a 404 error
    if not user:
        raise HTTPException(
            status_code=400,
            detail="User not found"
        )

    # Validate the role
    if new_role not in AccessLevelBase:
        raise HTTPException(
            status_code=400,
            detail="Invalid role"
        )

    # Update the user's role
    stmt = (
        update(User)
        .where(User.email == user_email)
        .values(user_role=new_role.value)
        .execution_options(synchronize_session="fetch")
    )
    await db.execute(stmt)
    await db.commit()

    return {"message": f"User role updated to {new_role.name}"}