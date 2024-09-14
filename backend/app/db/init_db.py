# Built-in Dependencies
import asyncio

# Third-Party Dependencies
from sqlmodel import select

# Local Dependencies
from app.db.session import async_engine as engine
from app.core.hashing import Hasher
from app.db.models.common import Base
from app.db.models.user import User
from app.db.models.organization import Organization
from app.db.models.role import Role
from app.db.models.member import Member


async def init_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def init_db() -> None:
    await init_tables()
