from typing import Dict, Any, Literal, Union

# Third-Party Dependencies
from sqlmodel.ext.asyncio.session import AsyncSession

# Local Dependencies
from app.db.crud.base import CRUDBase
from app.db.models.member import Member
from app.db.schemas.v1.schema_member import (
    MemberCreateInternal,
    MemberUpdate,
    MemberUpdateInternal,
    MemberDelete,
    MemberCreate,
    MemberRead
)

from app.core.http_exceptions import (
    DuplicateValueException,
    NotFoundException,
    ForbiddenException,
    # RateLimitException
)

from app.core.hashing import Hasher

CRUDMember = CRUDBase[
    Member, MemberCreateInternal, MemberUpdate, MemberUpdateInternal, MemberDelete
]

crud_member = CRUDMember(Member)


async def create_new_member(member: MemberCreate, db: AsyncSession) -> MemberRead:
    memberName_row = await crud_member.exists(db=db, memberName=member.memberName)
    if memberName_row:
        raise DuplicateValueException("Member is already registered")

    member_internal_dict = member.model_dump()

    member_internal = MemberCreateInternal(**member_internal_dict)
    return await crud_member.create(db=db, object=member_internal)

async def get_member(memberName: str, db: AsyncSession) -> Union[Dict[str, Any], Literal[None]]:
    db_member: dict = await crud_member.get(
            db=db, memberName=memberName, is_deleted=False
    )
    if not db_member:
        return None
    
    return db_member