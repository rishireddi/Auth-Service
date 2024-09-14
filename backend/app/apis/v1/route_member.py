#Third-Part Dependencies
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

#Local Dependencies
from app.db.crud.crud_member import crud_member, create_new_member 
from app.db.crud.crud_organization import crud_organization
from app.db.schemas.v1.schema_member import MemberCreate
from app.core.dependencies import async_get_db
from app.core.dependencies import CurrentUser
from fastapi import Depends, Request
from typing import Annotated, Dict
from app.core.http_exceptions import (
    DuplicateValueException,
    NotFoundException,
    ForbiddenException,
    # RateLimitException
)

router = APIRouter(tags=["Members"])

@router.post("/invite-member")
async def invite_member(
    member_data: MemberCreate,
    current_user: CurrentUser,
    db: AsyncSession = Depends(async_get_db)
):
    if current_user["user_role"] != 100:
        raise HTTPException(status_code=403, detail="Not authorized to invite members.")
    
    org = await crud_organization.get(db=db, id=member_data.org_id)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found.")

    await create_new_member(member_data, db)
    
    return {"message": "Member invited successfully."}


@router.delete("/delete_member")
async def erase_db_member(
    request: Request,
    memberName: str,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    current_user: CurrentUser
) -> Dict[str, str]:
    db_member = await crud_member.exists(db=db, memberName=memberName)
    if not db_member:
        raise NotFoundException("Member not found")

    await crud_member.db_delete(db=db, memberName=memberName)
    return {"message": "Member deleted from the database"}
