from sqlalchemy.orm import Session
from models.role.users_permissions_model import RoleUsers, RolePermissions
from models.user.user_model import User
from models.permission.permission_model import Permission


def get_user_has_been_bound(db: Session, role_id: int):
    """
    需要查询RoleUsers这个表
    获取改角色上，已经绑定的用户列表
    :param db:
    :param role_id:
    :return:
    """
    role_users = db.query(RoleUsers).filter(RoleUsers.role_id == role_id).all()
    bound_users = []
    if role_users:
        for role_user in role_users:
            user_id = role_user.user_id
            bound_users.append(user_id)
    return bound_users


def get_unbound_users(db: Session, role_id: int, bound_users):
    """
    获取没有停用的用户，并且排除已经绑定的用户，获取没有绑定的用户列表
    :param db:
    :param role_id:
    :return:
    """
    # 获取没有停用的用户信息
    no_deactivated_users = db.query(User).filter(User.state == 1).all()
    unbound_users = []
    bound_users = bound_users
    if no_deactivated_users:
        for no_deactivated_user in no_deactivated_users:
            if no_deactivated_user.id not in bound_users:
                unbound_user = {
                    "unbound_user_id": no_deactivated_user.id,
                    "unbound_user_name": no_deactivated_user.username
                }
                unbound_users.append(unbound_user)
    return unbound_users


def get_bound_and_unbound_users(db: Session, role_id: int):
    """
    给角色绑定用户的时候，需要获取已绑定用户和未绑定用户
    :param db:
    :param role_id:
    :return:
    """
    # 该角色上已绑定的用户：bound_users
    bound_users = get_user_has_been_bound(db, role_id)
    # 该角色上未绑定的用户:unbound_users
    unbound_users = get_unbound_users(db, role_id, bound_users)
    return {"bound_users": bound_users, "unbound_users": unbound_users}


def add_role_users(db: Session, role_id: int, users: [str]):
    """
    增加角色和用户的绑定
    :param db:
    :param role_id:
    :param users:
    :return:
    """
    # 先查询绑定role的所有用户
    role_user_deletes = db.query(RoleUsers).filter(RoleUsers.role_id == role_id).all()
    # 然后删除绑定
    if role_user_deletes:
        for role_user_delete in role_user_deletes:
            db.delete(role_user_delete)
    # 再进行增加
    role_users_add = []
    if users:
        for user_id in users:
            role_user = RoleUsers(
                role_id=role_id,
                user_id=user_id,
            )
            role_users_add.append(role_user)
    # 增加多条数据
    db.add_all(role_users_add)
    db.commit()
    db.flush()


def get_permissions_tree(db: Session, role_id: int):
    """
    获取权限树的信息
    :param db:
    :param role_id:
    :return:
    """
    tree = []
    # 获取所有的一级菜单：parent_id =0
    first_level_perms = db.query(Permission).order_by(Permission.sort.desc()).filter(Permission.parent_id == 0).all()
    for first_level in first_level_perms:
        first_menu = {
            "id": first_level.id,
            "name": first_level.name,
            "children": []
        }
        # 拿到该一级菜单的二级菜单
        children = db.query(Permission).filter(Permission.parent_id == first_level.id).all()
        if children:
            # todo 将返回的结果添加到children下
            first_menu["children"] = (get_children(db, children))
        tree.append(first_menu)
    return tree


def get_children(db: Session, children: [Permission]):
    """
    使用无限递归查询，查询一级菜单下，所有的子菜单
    :param db:
    :param children:
    :return:
    """
    son_children = []
    for child in children:
        next_menu = {
            "id": child.id,
            "name": child.name,
            "children": []
        }
        next_children = db.query(Permission).filter(Permission.parent_id == child.id).all()
        if next_children:
            # 在这里进行递归
            next_menu["children"] = (get_children(db, next_children))
        son_children.append(next_menu)
    return son_children


def get_permission_ids_by_role_id(db: Session, role_id: int):
    """
    根据role_id获取所有的权限id：权限id列表
    :param db:
    :param role_id:
    :return:
    """
    permissions = db.query(RolePermissions.perm_id).filter(RolePermissions.role_id == role_id).all()
    permission_ids = []
    for permission in permissions:
        permission_ids.append(permission.perm_id)

    return permission_ids


def add_role_permission(db: Session, role_id: int, perms: [str]):
    """
    将权限，绑定对应的role上
    :param db:
    :param role_id:
    :param perms:
    :return:
    """
    role_perms_deletes = db.query(RolePermissions).filter(RolePermissions.role_id == role_id).all()
    if role_perms_deletes:
        for role_perms_delete in role_perms_deletes:
            db.delete(role_perms_delete)
    role_perms_add = []
    if perms:
        for perm in perms:
            role_user = RolePermissions(
                role_id=role_id,
                perm_id=perm,
            )
            role_perms_add.append(role_user)
    db.add_all(role_perms_add)
    db.commit()
    db.flush()


def get_role_id_by_user_id(db: Session, user_id: int):
    tree = []
    # 一个用户可以分配多个角色，根据token拿到user_id，查询这个user下，绑定了什么role
    user_bound_roles = db.query(RoleUsers.role_id).filter(RoleUsers.user_id == user_id).all()
    for user_bound_role in user_bound_roles:
        role_id = user_bound_role.role_id
        # 再通过role_id拿到permission权限列表
        role_permissions = db.query(RolePermissions.perm_id).filter(RolePermissions.role_id == role_id).all()
        for role_permission in role_permissions:
            permission_id = role_permission.perm_id
            # 查一级菜单
            first_level_perms = db.query(Permission).filter(Permission.id == permission_id,
                                                            Permission.parent_id == 0).all()
            for first_level in first_level_perms:
                if first_level.name == "首页":
                    first_menu = {
                        "icon": first_level.icon,
                        "index": first_level.url,
                        "title": first_level.name
                    }
                else:
                    first_menu = {
                        "icon": first_level.icon,
                        "index": first_level.url,
                        "title": first_level.name,
                        "subs": []
                    }

                children = db.query(Permission).filter(Permission.parent_id == first_level.id).all()

                if children:
                    # todo 将返回的结果添加到children下
                    first_menu["subs"] = (get_menu_children(db, children))
                tree.append(first_menu)

        return tree


# 递归获取所有的子解点，无限递归
def get_menu_children(db: Session, children: [Permission]):
    son_children = []

    for child in children:
        next_menu = {
            "index": child.url,
            "title": child.name,
            "subs": []
        }

        next_children = db.query(Permission).filter(Permission.parent_id == child.id).all()

        if next_children:
            next_menu["subs"] = (get_menu_children(db, next_children))
        else:
            next_menu.pop("subs")

        son_children.append(next_menu)

    return son_children
