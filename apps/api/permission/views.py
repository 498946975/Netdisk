from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session
from utils import token
from db.get_db import get_db
from utils.permission_operation import *
from fastapi.responses import JSONResponse
from models.permission.permission_ret import PermissionRet
from models.department.department_ret import DepartmentRet

router = APIRouter(
    prefix="/permission"
)


@router.get("/permission_list", tags=["权限模块"])
def get_permission_list(page_size: int, current_page: int, id: str = Depends(token.parse_token),
                        db: Session = Depends(get_db)):
    permissions = get_permission_pagenation(db, page_size, current_page)

    permission_rets = []
    for permission in permissions:
        # 当前端和字段和后端数据库存储不一致当时候，需要新起一个模型，把后端的表格，重新赋值给前端
        # 注意：PermissionRet实例化得放在循环中，保证每次循环里面都是空的
        permission_ret = PermissionRet()
        permission_ret.id = permission.id
        permission_ret.name = permission.name
        permission_ret.url = permission.url
        permission_ret.method = permission.method
        permission_ret.args = permission.args
        permission_ret.desc = permission.desc
        permission_ret.create_time = permission.create_time
        # 根据级别的id，返回父级别的名称
        if permission.parent_id == 0:
            permission_ret.level = "1级"
            permission_ret.parent_name = "无"
        else:
            permission_ret.level = "2级"
            p = get_permission_by_id(db, permission.parent_id)
            permission_ret.parent_name = p.name

        permission_rets.append(permission_ret)

    total = get_permission_total(db)
    content = {
        "permissions": permission_rets,
        "pageSize": page_size,
        "pageTotal": total,
        "currentPage": current_page
    }
    return content


@router.get("/get_no_parents", tags=["权限模块"])
def get_no_parents(id: int, user_id: str = Depends(token.parse_token),
                   db: Session = Depends(get_db)):
    """
    编辑权限所依赖的下拉框，拿到除了当前父级别的，所有父级别
    :param id:
    :param user_id:
    :param db:
    :return:
    """
    parents = get_no_parent_names(db, id)
    parents_name = []
    for parent in parents:
        parents_name.append(parent.name)
    return {"code": 200, "msg": "查询成功", "parents_name": parents_name}


@router.post("/edit", tags=["权限模块"])
def edit(
        id: int = Form(...),
        name: str = Form(...),
        url: str = Form(...),
        method: str = Form(...),
        args: str = Form(None),
        parent_name: str = Form(...),
        desc: str = Form(...),
        icon: str = Form(...),
        user_id: str = Depends(token.parse_token),
        db: Session = Depends(get_db)):
    """
    编辑权限数据
    :param id:
    :param name:
    :param url:
    :param method:
    :param args:
    :param parent_name: 展示父级菜单的名称，parent_id=0的所有数据
    :param desc:
    :param icon:
    :param user_id:
    :param db:
    :return:
    """
    permission_update(db, id, name, url, method, args, parent_name, desc, icon)
    return {"code": 200, "msg": "更新成功", "id": id}


@router.post("/delete", tags=["权限模块"])
def delete_permission(permission: PermissionRet, user_id: str = Depends(token.parse_token),
                      db: Session = Depends(get_db)):
    """
    根据权限id，删除权限信息，如果删除的父权限有子权限进行了关联，则无法删除父权限
    :param permission:
    :param user_id:
    :param db:
    :return:
    """
    id = permission.id
    parents = get_all_parent_info(db)
    all_parents_id = []
    for parent in parents:
        all_parents_id.append(parent.parent_id)
    if id not in all_parents_id:
        delete_permission_by_id(db, id)
        return JSONResponse(content={"code": 200, "msg": "删除成功", "id": id})
    else:
        return JSONResponse(content={"code": 500, "msg": "无法删除，因为改菜单有子菜单关联"})


@router.get("/get_parents", tags=["权限模块"])
def get_parents(user_id: str = Depends(token.parse_token),
                db: Session = Depends(get_db)):
    """
    增加权限依赖的下拉框，获取所有的级别的名称
    :param user_id:
    :param db:
    :return:
    """
    parents = get_all_parent_info(db)
    parents_names = []
    for parent in parents:
        parents_names.append(parent.name)
    return {"code": 200, "msg": "更新成功", "parents": parents}


@router.post("/add", tags=["权限模块"])
def add(
        name: str = Form(...),
        url: str = Form(...),
        method: str = Form(...),
        args: str = Form(None),
        parent_name: str = Form(...),
        desc: str = Form(...),
        icon: str = Form(...),
        user_id: str = Depends(token.parse_token),
        db: Session = Depends(get_db)):
    """
    增加权限信息
    :param name:
    :param url:
    :param method:
    :param args:
    :param parent_name:
    :param desc:
    :param icon:
    :param user_id:
    :param db:
    :return:
    """
    add_permission(db, name, url, method, args, parent_name, desc, icon)
    return JSONResponse(content={"code": 200, "msg": "添加成功"})
