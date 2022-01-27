import secrets
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings, EmailStr, HttpUrl, PostgresDsn, validator


class Settings(BaseSettings):
    # JWT 相关
    ALGORITHM: str = "HS256"
    SECRET_KEY: str = secrets.token_urlsafe(32) # 随机生成base64位字符串
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # token过期时间

    # 项目名称相关
    TITLE: Optional[str] = "Netdisk"
    SERVER_HOST: AnyHttpUrl = "http://127.0.0.1:8001"
    DESC: Optional[str] = "网盘系统后端"

    # DB相关
    DB_USERNAME = "root"
    DB_PWD = "123"
    DB_TEST_HOST = "172.16.120.44"
    DB_PRO_HOST = ""
    DB_PORT = "3306"
    DB_NAME = "test_fastapi"
    DB_TEST_URL = "mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8".format(DB_USERNAME, DB_PWD, DB_TEST_HOST, DB_PORT, DB_NAME)
    DB_PRO_URL = "mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8".format(DB_USERNAME, DB_PWD, DB_PRO_HOST, DB_PORT, DB_NAME)



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
