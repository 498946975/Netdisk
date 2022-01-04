from datetime import datetime, timedelta
from typing import List, Optional
from fastapi import Depends, FastAPI, HTTPException, Security, status
from fastapi.security import (OAuth2PasswordRequestForm, SecurityScopes, OAuth2AuthorizationCodeBearer,
                              OAuth2PasswordRequestFormStrict)
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, ValidationError
from fastapi.responses import RedirectResponse

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRRSH_ACCESS_TOKEN_EXPIRE_MINUTES = 70

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    # 授权认证的URL地址
    authorizationUrl='/oauth2/authorize',
    # 配置授权的请求的是进行授权处理的接口地址
    tokenUrl="access_token",  #
    # 刷新获取新的token的地址
    refreshUrl='refreshUrl',
    # 定义我们的操作文档显示授权码授权区域----这个和下面的授权的区域关联起来，表示某个接口需要的授权域
    scopes={
        "get_admin_info": "获取管理员用户信息",
        "del_admin_info": "删除管理员用户信息",
        "get_user_info": "获取用户信息",
        "get_user_role": "获取用户所属角色信息",
        "get_user_permission": "获取用户相关的权限信息",

    }
)

# 加密方案
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 用户信息表
fake_users_db = {
    "xiaozhongtongxue": {
        "username": "xiaozhongtongxue",
        "full_name": "xiaozhongtongxue",
        "email": "xxxxxxxxx@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False
    }
}


class TokenData(BaseModel):
    username: Optional[str] = None
    scopes: List[str] = []


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class UserInDB(User):
    hashed_password: str


# 定义我们的APP服务对象
app = FastAPI()


# 获取加盐密码
def get_password_hash(password):
    return pwd_context.hash(password)


# 进行用户认证用户的认证
def authenticate_user(fake_db, username: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    return user


# 从上面定义的字典表里查询用户信息，并返回用户信息实体
def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


# 创建我们的授权之后，给用户签发的TOKEN
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    '''
    签发token
    :param data: data里面包含用户信息和签发授权的作用域信息
    :param expires_delta:
    :return:
    '''
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme)):
    print("当前认证方案里面的作用域：", security_scopes.scope_str)
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = f"Bearer"

    # 定义认证异常信息
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    print("当前携带上来的token值：", token)
    try:
        # 开始反向解析我们的TOKEN.,解析相关的信息
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        wxopenid: str = payload.get("sub")
        if wxopenid is None:
            raise credentials_exception

        print("当前用户名称userid：", wxopenid)
        token_scopes = payload.get("scopes", [])
        #
        print("当前用户所属的toekn信息里面包含的scopes信息有：", token_scopes)
        token_data = TokenData(scopes=token_scopes, username=wxopenid)
        print("token_data", token_data)
    except (JWTError, ValidationError):
        raise credentials_exception

    # 再一次从数据库里面验证用户信息
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception

    # 然后
    print("当前认证方案里面所有security_scopes信息有：", security_scopes.scopes)
    for scope in security_scopes.scopes:
        # 对比用户的token锁携带的用户的作用区域授权信息
        if scope not in token_data.scopes:
            # 如果不存在则返回没有权限异常信息
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user


# 注意接口的也可以定义相关的权限的依赖！！！！或者组合的，比如我这里要是定义其他的话，依赖这个的接口，如果没有这个权限也无法访问！
async def get_current_active_user(current_user: User = Security(get_current_user, scopes=["get_admin_info"])):
    print("输出当前用户：", current_user)
    # 判断用书是否已经被禁用了！！！如果没有则继续执行
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.get("/access_token")
async def access_token(appid: Optional[str], secret: Optional[str], code: Optional[str],
                       grant_type: Optional[str] = 'authorization_code'):
    # 开始签发我们的toeken和refresh_token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    scopes = ['get_admin_info', 'del_admin_info']
    # print('当前写入的作用去scopes：', scopes)

    # 验证code和appid 信息
    if code == 'SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS' and appid == 'xiaozhongtongxue' and secret == 'xiaozhongtongxue':
        pass
        # 这里仅仅作为演示，相关的处理逻辑需要结合业务来进行处理

    # 因为需要对用户的信息再核查这里直接传这个
    username = 'xiaozhongtongxue'

    access_token = create_access_token(
        data={"sub": username, "scopes": scopes},
        expires_delta=access_token_expires,
    )
    # 刷新refresh_token过期的时间
    refresh_access_token_expires = timedelta(minutes=REFRRSH_ACCESS_TOKEN_EXPIRE_MINUTES)
    # 刷新refresh_token
    refresh_token = create_access_token(
        data={"sub": appid, "scopes": scopes},
        expires_delta=refresh_access_token_expires,
    )

    return {
        "access_token": access_token,
        # access_token接口调用凭证超时时间
        "expires_in": access_token_expires,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "userid": username,
        "scope": "SCOPE"
    }


# 必须使用GET的请求才可以
@app.get("/oauth2/authorize")
async def authorizationUrl(appid: Optional[str], redirect_uri: Optional[str], scopes: str = None,
                           response_type: Optional[str] = 'code'):
    # 开始对这个用户对应的信息验证处理，然后生产我们的code
    user = authenticate_user(fake_users_db, appid)
    if not user:
        raise HTTPException(status_code=400, detail="合作方APPID不存在")

    # 假设用户这地方默认接收我们的授权请求的处理！！！！！！--如果是网页的，可以还是需要其他的接口进行转接一下

    # 默认---同意授权-----省略网页显示授权页面

    # 开始返回我们的对应的针对于我们的当前特点的合作方分配不同的code----
    # 注意这个地方我只是为了演示，这个地方肯定是需要生成不一样的code来处理的哟！而且是和我们的appid一一对应的
    code = 'SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS'
    # 开始进行回调
    return RedirectResponse(url=redirect_uri + "?code=" + code)


@app.get("/status/")
async def read_system_status():
    return {"status": "ok"}


@app.get("/typer")
async def redirect_typer():
    return RedirectResponse("https://typer.tiangolo.com")


@app.get("/api/v1/get_admin_info", response_model=User)
async def get_admin_info(current_user: User = Security(get_current_active_user, scopes=["get_admin_info"])):
    return current_user


@app.get("/api/v1/del_admin_info", response_model=User)
async def del_admin_info(current_user: User = Security(get_current_active_user, scopes=["del_admin_info"])):
    return current_user


@app.get("/api/v1/get_user_info", response_model=User)
async def get_user_info(current_user: User = Security(get_current_active_user, scopes=["get_user_info"])):
    return current_user


@app.get("/api/v1/get_user_role", response_model=User)
async def get_user_role(current_user: User = Security(get_current_active_user, scopes=["get_user_role"])):
    return current_user


@app.get("/api/v1/get_user_permission", response_model=User)
async def get_user_role(current_user: User = Security(get_current_active_user, scopes=["get_user_permission"])):
    return current_user


import uvicorn

if __name__ == '__main__':
    # 等于通过 uvicorn 命令行 uvicorn 脚本名:app对象 启动服务：uvicorn xxx:app --reload
    uvicorn.run('OAuth2AuthorizationCodeBearer-test:app', host="127.0.0.1", port=8000, debug=True, reload=True)
