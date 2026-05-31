import os
from pathlib import Path
from pydantic import PostgresDsn
from pydantic import BaseModel
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)

BASE_DIR = Path(__file__).resolve().parent.parent


class CalendarSchedule(BaseModel):
    calendar_schedule_limit_days: int = 30


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


class TestDatabaseConfig(BaseModel):
    url: str = (
        "postgresql+asyncpg://pguser_test:pgpassword_test@db_test:5432/syncslot_db_test"
    )


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


class ApiV1Tags(BaseModel):
    tag_company_auth: str = "company auth"
    tag_company_settings: str = "company settings"
    tag_company_work_schedule: str = "company work schedule"
    tag_company_logo_image: str = "company logo image"
    tag_company_service: str = "company service"
    tag_company_service_public: str = "company service public"
    tag_company_booking_schedule: str = "company booking schedule"
    tag_booking: str = "booking"
    tag_client_auth: str = "client auth"
    tag_client_booking: str = "client booking"
    tag_company: str = "company"


class ApiV1Prefix(BaseModel):
    prefix_company_auth: str = "/api/v1/company/auth"
    prefix_company_settings: str = "/api/v1/company/settings"
    prefix_company_work_schedule: str = "/api/v1/company/work-schedule"
    prefix_company_logo_image: str = "/api/v1/company/logo-image"
    prefix_company_service: str = "/api/v1/company/service"
    prefix_company_service_public: str = "/api/v1/company/service/public"
    prefix_company_booking_schedule: str = "/api/v1/company/booking/schedule"
    prefix_booking: str = "/api/v1/booking"
    prefix_client_auth: str = "/api/v1/client/auth"
    prefix_client_booking: str = "/api/v1/client/booking"
    prefix_list_companies: str = "/api/v1/list-companies"
    prefix_company_by_slug: str = "/api/v1/company-by-slug"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(
            os.path.join(BASE_DIR, ".env"),
            os.path.join(BASE_DIR, ".env_example"),
        ),
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="SYNC_SLOT__",
    )
    run: RunConfig = RunConfig()
    api_v1: ApiV1Prefix = ApiV1Prefix()
    tags: ApiV1Tags = ApiV1Tags()
    db: DatabaseConfig
    db_test: TestDatabaseConfig = TestDatabaseConfig()
    jwt: JWT = JWT()
    password: Password = Password()
    file_company_logo_settings: FileCompanyLogoSettings = FileCompanyLogoSettings()
    booking_url: BookingUrl = BookingUrl()
    calendar_schedule: CalendarSchedule = CalendarSchedule()


settings = Settings()
