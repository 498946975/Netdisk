from fastapi import Depends, Request, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from functools import reduce
from db.get_db import get_db
from utils.get_md5_data import get_md5_pwd
from utils.user_operation import get_user_by_username_and_pwd, get_user_by_id, update_time_and_ip
from fastapi.responses import JSONResponse
from utils import token
from datetime import timedelta
from utils.users_permission_operation import get_role_id_by_user_id
import datetime

router = APIRouter(
    prefix="/login"
)

# token过期时间
EXPIRE_MINUTE = 1440


@router.post("/", tags=["登录模块"])
def Login(request: Request, user: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # 1.用户信息获取
    username = user.username
    pwd = user.password
    # 密码加密
    md5_pwd = get_md5_pwd(pwd)

    # 2.数据库校验
    user = get_user_by_username_and_pwd(db, username, md5_pwd)

    if user:
        # 停用的不让登录
        if user.state == 2:
            content = {"code": 500, "msg": "该用户已停用,请联系管理员!"}
            return JSONResponse(content=content)
        # 用户删除，不让登陆
        if user.is_delete == 1:
            content = {"code": 500, "msg": "该用户已删除,请联系管理员!"}
            return JSONResponse(content=content)
        # 启用的正常执行
        # 3.token生成
        expire_time = timedelta(minutes=EXPIRE_MINUTE)
        ret_token = token.create_token({"sub": str(user.id)}, expire_time)

        # 4.返回token及用户信息

        # 日期格式需要转成字符串
        ret_user = {"username": user.username, "avatar": user.avatar, "ip": user.ip,
                    "last_login_date": user.last_login_date.strftime("%Y-%m-%d")}
        login_date = datetime.datetime.now()
        ip = request.client.host
        update_time_and_ip(db, user.id, login_date, ip)
        content = {"code": 200, "msg": "登录成功", "token": ret_token, "user": ret_user}
        return JSONResponse(content=content)
    else:
        content = {"code": 500, "msg": "用户名或密码错误"}
        return JSONResponse(content=content)


@router.get("/index", tags=["首页模块"])
def Index(id: str = Depends(token.parse_token), db: Session = Depends(get_db)):
    # 根据token解析出来的id查询数据库
    user = get_user_by_id(db, int(id))
    return user


@router.get("/get_menus", tags=["首页模块"])
def get_menus(
        user_id: str = Depends(token.parse_token),
        db: Session = Depends(get_db)):
    """
    根据用户的ID，获取角色权限，实现动态展示首页功能菜单
    :param id:
    :param db:
    :return:
    """
    # 根据token拿到user_id，查询这个user下，绑定了什么role
    tree = get_role_id_by_user_id(db, int(user_id))

    # Google一下：python 列表中的字典去重
    # 对重复的权限进行去重
    run_function = lambda x, y: x if y in x else x + [y]
    set_tree = reduce(run_function, [[], ] + tree)
    # todo 假如tree为空，也就是没有权限，跳转到没有权限的页面
    return {"code": 200, "msg": "查询成功", "tree": set_tree}
