from pydantic import BaseModel
from typing import Optional


# Optional的意思是可以为空
class UserRet(BaseModel):
    id: Optional[int]
    # 用户名
    username: Optional[str]
    # 密码
    pwd: Optional[str]
    # todo 部门外键
    dep_id: Optional[int]

    # 头像
    avatar: Optional[str]
    # 地址
    addr: Optional[str]
    # 状态,1表示启用，2表示停用
    state: Optional[int]
    # 上次登录日期
    last_login_date: Optional[str]
    # 上次登录的IP地址
    ip: Optional[str]

    # 创建时间: 年月日 时分秒
    create_time: Optional[str]
    # 创建日期：年月日
    create_date: Optional[str]
