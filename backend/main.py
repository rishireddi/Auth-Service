import sys
import os

import fastapi
import uvicorn

# Add the project directory to the sys.path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))


# Our Libs
from app.core.config import settings
from app.db import init_db
from app.apis.base import api_router

description = """
Auth Service for Multi tenant Saas
## API Supported
- User Details
- Organization
- Member
- Role

"""
tags_metadata = [
    {"name": "Login", "description": "This is user login route"},
    {"name": "User", "description": "This is user route"},
    {"name": "Member", "description": "This is Member route"},
    {"name": "Organization", "description": "This is Organization route"},
    {"name": "Role", "description": "This is Role route"},
]


def include_router(app: fastapi.FastAPI):
    app.include_router(api_router)



async def startup_event():
    print("Executing startup event")
    await init_db.init_db()


def start_application():
    app = fastapi.FastAPI(
        title=settings.PROJECT_TITLE,
        version=settings.PROJECT_VERSION,
        description=description,
        contact={"name": settings.CONTACT_NAME, "email": settings.CONTACT_EMAIL},
    )
    include_router(app)
    app.add_event_handler("startup", startup_event)
    return app


if __name__ == "__main__":
    # app = start_application()
    try:
        print(f"[INFO] Starting Application at: host={settings.SERVER_IP}, port={settings.SERVER_PORT}")
        uvicorn.run(
            "main:start_application",
            host=settings.SERVER_IP,
            port=settings.SERVER_PORT,
            reload=True,
        )
    except Exception as e:
        print(f"[ERROR] Main Error: {e}")
