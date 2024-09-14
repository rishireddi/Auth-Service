# Local Dependencies
from app.db.schemas.v1.schema_auth import (
    TokenBlacklistCreate,
    TokenBlacklistUpdate,
)
from app.db.models.auth import TokenBlacklist
from app.db.crud.base import CRUDBase

# Define a CRUD (Create, Read, Update, Delete) interface for the TokenBlacklist model
CRUDTokenBlacklist = CRUDBase[
    TokenBlacklist,
    TokenBlacklistCreate,
    TokenBlacklistUpdate,
    TokenBlacklistUpdate,
    None,
]

# Create an instance of the CRUDTokenBlacklist with the TokenBlacklist model
crud_token_blacklist = CRUDTokenBlacklist(TokenBlacklist)
