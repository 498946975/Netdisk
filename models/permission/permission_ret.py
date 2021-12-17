from pydantic import BaseModel
from typing import Optional


class PermissionRet(BaseModel):
    # 字段必须和前端一一对应
    id: Optional[int]
    name: Optional[str]
    url: Optional[str]
    method: Optional[str]
    args: Optional[str]
    # 父级别菜单名称
    parent_name: Optional[str]
    # 级别
    level: Optional[str]
    desc: Optional[str]
    create_time: Optional[str]
