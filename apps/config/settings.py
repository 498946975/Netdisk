import secrets
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings, EmailStr, HttpUrl, PostgresDsn, validator


class Settings(BaseSettings):
    API_V1_STR: str = "/edp-query-py/V1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    SERVER_NAME: str = "fastapi-test"
    SERVER_HOST: AnyHttpUrl = "http://127.0.0.1:8001"
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ['http://127.0.0.1:8080', 'http://localhost:8080']
    PROJECT_NAME: str = "fastapi-test"
    # @validator("BACKEND_CORS_ORIGINS", pre=True)
    # def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
    #     if isinstance(v, str) and not v.startswith("["):
    #         return [i.strip() for i in v.split(",")]
    #     elif isinstance(v, (list, str)):
    #         return v
    #     raise ValueError(v)
    #

    #
    DB_USERNAME = "root"
    DB_PWD = "123"
    DB_PRO_HOST = "81.70.88.52"
    DB_TEST_HOST = "172.16.120.44"
    DB_PORT = "3306"
    DB_NAME = "test_fastapi"
    DB_TEST_URL = "mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8".format(DB_USERNAME, DB_PWD, DB_TEST_HOST, DB_PORT, DB_NAME)
    DB_PRO_URL = "mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8".format(DB_USERNAME, DB_PWD, DB_PRO_HOST, DB_PORT, DB_NAME)
    #
    #
    # @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    # def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
    #     if isinstance(v, str):
    #         return v
    #     return PostgresDsn.build(
    #         scheme="postgresql",
    #         user=values.get("POSTGRES_USER"),
    #         password=values.get("POSTGRES_PASSWORD"),
    #         host=values.get("POSTGRES_SERVER"),
    #         path=f"/{values.get('POSTGRES_DB') or ''}",
    #     )
    #
    # SMTP_TLS: bool = True
    # SMTP_PORT: Optional[int] = None
    # SMTP_HOST: Optional[str] = None
    # SMTP_USER: Optional[str] = None
    # SMTP_PASSWORD: Optional[str] = None
    # EMAILS_FROM_EMAIL: Optional[EmailStr] = None
    # EMAILS_FROM_NAME: Optional[str] = None
    #
    # @validator("EMAILS_FROM_NAME")
    # def get_project_name(cls, v: Optional[str], values: Dict[str, Any]) -> str:
    #     if not v:
    #         return values["PROJECT_NAME"]
    #     return v
    #
    # EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48
    # EMAIL_TEMPLATES_DIR: str = "/app/app/email-templates/build"
    # EMAILS_ENABLED: bool = False
    #
    # @validator("EMAILS_ENABLED", pre=True)
    # def get_emails_enabled(cls, v: bool, values: Dict[str, Any]) -> bool:
    #     return bool(
    #         values.get("SMTP_HOST")
    #         and values.get("SMTP_PORT")
    #         and values.get("EMAILS_FROM_EMAIL")
    #     )
    #
    # EMAIL_TEST_USER: EmailStr = "test@example.com"  # type: ignore
    # FIRST_SUPERUSER: EmailStr = "admin@123.com"
    # FIRST_SUPERUSER_PASSWORD: str = "0p-0p-0p-"
    # USERS_OPEN_REGISTRATION: bool = False

    class Config:
        case_sensitive = True


settings = Settings()



# from pydantic import BaseSettings
#
#
# class Settings(BaseSettings):
#     app_name: str = "Awesome API"
#     admin_email = "123@qq.com"
#     items_per_user: int = 50
#
#
# settings = Settings()
