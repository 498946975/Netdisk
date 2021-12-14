from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta

crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# salt盐
SECRET_KEY = "123456"

ALGORITHM = "HS256"


# 明文密码加密
def get_hash_pwd(pwd: str):
    return crypt_context.hash(pwd)


# 生成token:用户数据，token过期时间
def create_token(data: dict, expire_time):
    if expire_time:
        expire = datetime.utcnow() + expire_time
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)

    data.update({"exp": expire})
    token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

    return token


oauth_scame = OAuth2PasswordBearer(tokenUrl="login")  # post请求，相对  /login


# token校验
def parse_token(token: str = Depends(oauth_scame)):
    token_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token不正确或已过期",
        headers={"WWW-Authenticate": "Beater"}
    )

    try:
        jwt_data = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        id = jwt_data.get("sub")
        if id is None or id == "":
            raise token_exception
    except JWTError:
        raise token_exception
    return id
