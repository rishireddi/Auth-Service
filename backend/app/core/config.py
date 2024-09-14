# Built-in Dependencies
from typing import Annotated, Any
from enum import Enum
import os

# Third-Party Dependencies
from pydantic import AnyUrl, BeforeValidator
from pydantic_settings import BaseSettings
from starlette.config import Config

current_file_dir = os.path.dirname(os.path.realpath(__file__))
env_path = os.path.abspath(os.path.join(current_file_dir, "..","..", ".env"))
config = Config(env_path)


def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)

def unset_env():
    all_env = os.environ
    if 'POSTGRES_SERVER' in all_env:
        del os.environ['POSTGRES_SERVER']
    if 'POSTGRES_PORT' in all_env:
        del os.environ['POSTGRES_PORT']
    if 'POSTGRES_USER' in all_env:
        del os.environ['POSTGRES_USER']
    if 'POSTGRES_PASSWORD' in all_env:
        del os.environ['POSTGRES_PASSWORD']
    if 'POSTGRES_DB' in all_env:
        del os.environ['POSTGRES_DB']
    if 'POSTGRES_ASYNC_URI' in all_env:
        del os.environ['POSTGRES_ASYNC_URI']
    if 'DATABASE_URL' in all_env:
        del os.environ['DATABASE_URL']

class AppSettings(BaseSettings):
    PROJECT_TITLE: str = config("PROJECT_TITLE", default="Auth Service for Multi tenant Saas")
    PROJECT_VERSION: str = config("PROJECT_VERSION", default="0.0.1")
    LICENSE_NAME: str = config("LICENSE_NAME", default=None)
    CONTACT_NAME: str = config("CONTACT_NAME", default="Rishitha Enumula")
    CONTACT_EMAIL: str = config(
        "CONTACT_EMAIL", default="rishitha.enumula@gmail.com"
    )
    SERVER_IP: str = config("SERVER_IP", default="127.0.0.1")
    SERVER_PORT: int = int(config("SERVER_PORT", default=9000))
    SERVER_LINK: str = config("", default=f"http://{SERVER_IP}:{SERVER_PORT}/")
    LOCAL_HOST: str = config("LOCAL_HOST", default="http://localhost")
    UI_SERVER_IP_PORT: str = config("UI_SERVER_IP_PORT", default="http://localhost:5173")

    COOKIES_SECURE_SETTINGS: bool = config("COOKIES_SECURE_SETTINGS", default=False)



class CryptSettings(BaseSettings):
    SECRET_KEY: str = config("SECRET_KEY", default="I_AM_WONDER_WOMAN")
    ALGORITHM: str = config("ALGORITHM", default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = config(
        "ACCESS_TOKEN_EXPIRE_MINUTES", default=1440
    )
    REFRESH_TOKEN_EXPIRE_DAYS: int = config("REFRESH_TOKEN_EXPIRE_DAYS", default=7)


class DatabaseSettings(BaseSettings):
    DATABASE_USER_TABLE: str = config("DATABASE_USER_TABLE", default="user_data")
    DATABASE_ORGANIZATION_TABLE: str = config("DATABASE_ORGANIZATION_TABLE", default="organization_data")
    DATABASE_ROLE_TABLE: str = config("DATABASE_ROLE_TABLE", default="role_data")
    DATABASE_MEMBER_TABLE: str = config("DATABASE_MEMBER_TABLE", default="member_data")

class PostgresSettings(DatabaseSettings):
    POSTGRES_USER: str = config("POSTGRES_USER", default="postgres")
    POSTGRES_PASSWORD: str = config("POSTGRES_PASSWORD", default="postgres")
    POSTGRES_SERVER: str = config("POSTGRES_SERVER", default="localhost")
    POSTGRES_PORT: int = config("POSTGRES_PORT", default=5432)
    POSTGRES_DB: str = config("POSTGRES_DB", default="postgres")
    POSTGRES_ASYNC_URI: str = (
        f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )
    DATABASE_URL:str = POSTGRES_ASYNC_URI



class API_Configs(BaseSettings):
    API_V1_BASE_PATH: str = config("API_V1_BASE_PATH", default="")
    API_V1_LOGIN_PREFIX: str = config("API_V1_LOGIN_PREFIX", default=f"{API_V1_BASE_PATH}/auth")
    API_V1_USER_PREFIX: str = config("API_V1_USER_PREFIX", default=f"{API_V1_BASE_PATH}/users")
    API_V1_COMPANY_PREFIX: str = config("API_V1_COMPANY_PREFIX", default=f"{API_V1_BASE_PATH}/company")
    
class Settings(
    AppSettings,
    PostgresSettings,
    CryptSettings,
    API_Configs,
):
    pass

unset_env()
settings = Settings()