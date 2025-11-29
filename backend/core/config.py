import os
from pathlib import Path
from pydantic import PostgresDsn
from pydantic import BaseModel
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)

BASE_DIR = Path(__file__).resolve().parent.parent

class BookingUrl(BaseModel):
    base_url: str = "https://syncslot.ru/booking"


class FileCompanyLogoSettings(BaseModel):
    path_file: str = os.path.join(BASE_DIR, "storage")
    valid_extensions: tuple = ("png", "jpg", "jpeg")
    max_file_size_mb: int = 5


class Password(BaseModel):
    salt: str = "Tom&Jerry"


class JWT(BaseModel):
    secret_key: str = "MickeyMouse"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440
    refresh_token_expire_minutes: int = 43200
    token_type_access: str = "access"
    token_type_refresh: str = "refresh"


class RunConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = 10004


class DatabaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class ApiV1Prefix(BaseModel):
    prefix_company: str = "/api/v1/company"
    prefix_service: str = "/api/v1/service"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(os.path.join(BASE_DIR, ".env"), os.path.join(BASE_DIR, ".env_example")),
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="SYNC_SLOT__",
    )
    run: RunConfig = RunConfig()
    api_v1: ApiV1Prefix = ApiV1Prefix()
    db: DatabaseConfig
    jwt: JWT = JWT()
    password: Password = Password()
    file_company_logo_settings: FileCompanyLogoSettings = FileCompanyLogoSettings()
    booking_url: BookingUrl = BookingUrl()


settings = Settings()
