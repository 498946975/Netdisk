from fastapi import APIRouter, Depends, Form
from utils import token
from db.get_db import get_db
from utils.role_operation import *

from fastapi.responses import JSONResponse

from models.department.department_ret import DepartmentRet

router = APIRouter(
    prefix="/role"
)


@router.get("/role_list", tags=["角色模块"])
def get_role_list(page_size: int, current_page: int, id: str = Depends(token.parse_token),
                  db: Session = Depends(get_db)):
    """
    角色信息的分页查询
    :param page_size:
    :param current_page:
    :param id:
    :param db:
    :return:
    """
    roles = get_role_pagenation(db, page_size, current_page)
    total = get_role_total(db)
    content = {
        "roles": roles,
        "pageSize": page_size,
        "pageTotal": total,
        "currentPage": current_page
    }
    return content


@router.post("/edit", tags=["角色模块"])
def edit(
        id: int = Form(...),
        name: str = Form(...),
        desc: str = Form(...),
        user_id: str = Depends(token.parse_token),
        db: Session = Depends(get_db)):
    """
    修改角色的信息
    :param id:
    :param name:
    :param desc:
    :param user_id:
    :param db:
    :return:
    """
    role_update(db, id, name, desc)
    return {"code": 200, "msg": "更新成功", "id": id}


@router.post("/delete", tags=["角色模块"])
def delete_department(department: DepartmentRet, user_id: str = Depends(token.parse_token),
                      db: Session = Depends(get_db)):
    """
    删除角色信息，硬删除
    :param department:
    :param user_id:
    :param db:
    :return:
    """
    id = department.id
    delete_role_by_id(db, id)
    return JSONResponse(content={"code": 200, "msg": "删除成功", "id": id})


@router.post("/add", tags=["角色模块"])
async def add(
        name: str = Form(...),
        desc: str = Form(...),
        user_id: str = Depends(token.parse_token),
        db: Session = Depends(get_db)):
    """
    增加角色信息
    :param name:
    :param leader:
    :param desc:
    :param user_id:
    :param db:
    :return:
    """
    add_role(db, name, desc)
    return JSONResponse(content={"code": 200, "msg": "添加成功"})


@router.get("/query", tags=["角色模块"])
def query(
        role_name: str,
        page_size: int,
        current_page: int,
        user_id: str = Depends(token.parse_token),
        db: Session = Depends(get_db)):
    """
    给角色名称，查询对应的信息
    :param role_name:
    :param page_size:
    :param current_page:
    :param user_id:
    :param db:
    :return:
    """
    if role_name == "" or role_name == None or role_name == '':

        roles = get_role_pagenation(db, page_size, current_page)
        total = get_role_total(db)
    else:
        role_name = role_name.strip()
        roles = query_role(db, role_name, page_size, current_page)
        total = get_role_query_totle(db, role_name)

    content = {
        "roles": roles,
        "pageSize": page_size,
        "pageTotal": total,
        "currentPage": current_page
    }
    return content


@router.get("/get_users", tags=["角色模块"])
def get_users(role_id: int, user_id: str = Depends(token.parse_token),
              db: Session = Depends(get_db)):
    ret_dict = get_db_users(db, role_id)

    return {"code": 200, "msg": "查询成功", "ret": ret_dict}


# 角色配置用户
@router.post("/user_pz", tags=["角色模块"])
def user_pz(
        id: int = Form(...),
        users: str = Form(...),
        user_id: str = Depends(token.parse_token),
        db: Session = Depends(get_db)):
    users = users.split(",")
    add_role_users(db, id, users)
    return {"code": 200, "msg": "用户配置成功", "id": id}


# 角色权限配置
@router.get("/get_permissions", tags=["角色模块"])
def get_permissions(
        role_id: int,
        user_id: str = Depends(token.parse_token),
        db: Session = Depends(get_db)):
    # tree = json.dumps(get_permissions_tree(db,role_id))
    tree = get_permissions_tree(db, role_id)

    perms = get_permission_ids_by_role_id(db, role_id)
    ret = {
        # 所有的权限树
        "tree": tree,
        # 角色上已配置的权限
        "checked": perms
    }
    return {"code": 200, "msg": "查询成功", "ret": ret}


# 角色配置用户
@router.post("/perm_pz", tags=["角色模块"])
def perm_pz(
        id: int = Form(...),
        perms: str = Form(...),
        user_id: str = Depends(token.parse_token),
        db: Session = Depends(get_db)):
    perms = perms.split(",")
    add_role_perms(db, id, perms)
    return {"code": 200, "msg": "权限配置成功", "id": id}


# 获取菜单
from functools import reduce


@router.get("/get_menus", tags=["角色模块"])
def get_menus(
        id: str = Depends(token.parse_token),
        db: Session = Depends(get_db)
):
    tree = get_role_id_by_user_id(db, int(id))

    # 对重复的权限进行去重
    run_function = lambda x, y: x if y in x else x + [y]

    set_tree = reduce(run_function, [[], ] + tree)
    # todo 假如tree为空，也就是没有权限，跳转到没有权限的页面
    return {"code": 200, "msg": "查询成功", "tree": set_tree}
