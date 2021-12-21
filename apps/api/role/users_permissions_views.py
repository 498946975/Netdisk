from fastapi import APIRouter, Depends, Form
from utils import token
from db.get_db import get_db
from utils.users_permission_operation import get_bound_and_unbound_users, \
    add_role_users, get_permissions_tree, get_permission_ids_by_role_id, \
    add_role_permission
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/users_permissions"
)


@router.get("/get_bound_and_unbound_users", tags=["绑定模块"])
def get_users(role_id: int, user_id: str = Depends(token.parse_token),
              db: Session = Depends(get_db)):
    """
    下拉框，返回已经绑定的角色和未绑定的角色
    :param role_id:
    :param user_id:
    :param db:
    :return:
    """
    ret_dict = get_bound_and_unbound_users(db, role_id)
    return {"code": 200, "msg": "查询成功", "ret": ret_dict}


@router.post("/user_bound", tags=["绑定模块"])
def user_bound(
        role_id: int = Form(...),
        users: str = Form(...),
        user_id: str = Depends(token.parse_token),
        db: Session = Depends(get_db)):
    """
    增加users和role的绑定关系
    :param role_id:
    :param users:
    :param user_id:
    :param db:
    :return:
    """
    users = users.split(",")
    add_role_users(db, role_id, users)
    return {"code": 200, "msg": "用户配置成功", "id": role_id}


@router.get("/get_permission_bound", tags=["绑定模块"])
def get_permission_bound(
        role_id: int,
        user_id: str = Depends(token.parse_token),
        db: Session = Depends(get_db)):
    """
    获取权限树，并根据role_id查询已经绑定的权限
    :param role_id:
    :param user_id:
    :param db:
    :return:
    """
    # 先获取权限树
    tree = get_permissions_tree(db, role_id)
    permission_ids = get_permission_ids_by_role_id(db, role_id)
    ret = {
        # 所有的权限树
        "tree": tree,
        # 角色上已配置的权限
        "bound": permission_ids
    }
    return {"code": 200, "msg": "查询成功", "ret": ret}


@router.post("/permission_bound", tags=["绑定模块"])
def permission_bound(
        role_id: int = Form(...),
        perms: str = Form(...),
        user_id: str = Depends(token.parse_token),
        db: Session = Depends(get_db)):
    """
    将选择好的权限，绑定到对应到role上
    :param role_id:
    :param perms:
    :param user_id:
    :param db:
    :return:
    """
    perms = perms.split(",")
    add_role_permission(db, role_id, perms)
    return {"code": 200, "msg": "权限配置成功", "id": role_id}
