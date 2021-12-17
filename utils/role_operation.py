from sqlalchemy.orm import Session
from models.role.role_model import Role
from models.user.user_model import User


# from models.permission.permission_model import Permission


def get_role_by_id(db: Session, id: int) -> Role:
    """
    根据角色id，返回角色的所有信息
    :param db:
    :param id:
    :return:
    """
    role = db.query(Role.id, Role.name, Role.desc, Role.create_time).filter(Role.id == id).first()

    return role


# SELECT * from `user` LIMIT (page-1)*pagesize,5
def get_role_pagenation(db: Session, page_size: int, current_page: int) -> [Role]:
    """
    角色的分页查询
    :param db:
    :param page_size:
    :param current_page:
    :return:
    """
    roles = db.query(
        Role.id,
        Role.name,
        Role.desc,
        Role.create_time
    ).limit(page_size).offset((current_page - 1) * page_size).all()
    return roles


def get_role_total(db: Session) -> int:
    """
    获取角色的总数
    :param db:
    :return:
    """
    total = db.query(Role).count()
    return total


def role_update(db: Session, id: int, name: str, desc: str):
    """
    角色内容的编辑
    :param db:
    :param id: 角色id
    :param name: 角色名称
    :param desc: 角色描述
    :return:
    """
    role = db.query(Role).filter(Role.id == id).first()
    role.name = name
    role.desc = desc
    db.commit()
    db.flush()


def delete_role_by_id(db: Session, id: int):
    """
    根据id，删除对应的角色
    :param db:
    :param id:
    :return:
    """
    department = db.query(Role).filter(Role.id == id).first()
    db.delete(department)
    db.commit()
    db.flush()


# 添加
def add_role(db: Session, name: str, desc: str):
    """
    添加角色信息
    :param db:
    :param name:
    :param desc:
    :return:
    """
    department = Role(
        name=name,
        desc=desc,

    )
    db.add(department)
    db.commit()
    db.flush()


def query_role(db: Session, role_name: str, page_size: int, current_page: int) -> [Role]:
    """
    给角色名称，返回角色信息
    :param db:
    :param role_name:
    :param page_size:
    :param current_page:
    :return:
    """
    departments = db.query(
        Role.id,
        Role.name,
        Role.desc,
        Role.create_time
    ).filter(Role.name.like('%' + role_name + '%')).limit(page_size).offset((current_page - 1) * page_size).all()
    return departments


def get_role_query_totle(db: Session, role_name: str) -> int:
    """
    根据角色名称，返回符合条件的个数
    :param db:
    :param q:
    :return:
    """
    total = db.query(Role).filter(Role.name.like('%' + role_name + '%')).count()
    return total


def get_db_users(db: Session, role_id: int):
    # 该角色上已绑定的用户：users
    role_users = db.query(RoleUsers).filter(RoleUsers.role_id == role_id).all()
    users = []
    if role_users:
        for role_user in role_users:
            user_id = role_user.user_id
            users.append(user_id)

    not_users = db.query(User).filter(User.state == 1).all()
    # 该角色上未绑定的用户:user_options
    user_options = []
    if not_users:
        for not_user in not_users:
            user_option = {
                "value": not_user.id,
                "label": not_user.username
            }

            user_options.append(user_option)

    return {"users": users, "user_options": user_options}


# 角色绑定用户
def add_role_users(db: Session, id: int, users: [str]):
    role_user_dels = db.query(RoleUsers).filter(RoleUsers.role_id == id).all()
    if role_user_dels:
        for role_user_del in role_user_dels:
            db.delete(role_user_del)

    role_users_add = []
    if users:
        for user_id in users:
            role_user = RoleUsers(
                role_id=id,
                user_id=user_id,
            )
            role_users_add.append(role_user)

    db.add_all(role_users_add)
    db.commit()
    db.flush()

# # 获取权限树
# def get_permissions_tree(db: Session, role_id: int):
#     tree = []
#     # 获取所有的一级菜单：parent_id =0
#     first_level_perms = db.query(Permission).order_by(Permission.sort.desc()).filter(Permission.parent_id == 0).all()
#
#     for first_level in first_level_perms:
#         first_menu = {
#             "id": first_level.id,
#             "label": first_level.name,
#             "children": []
#         }
#
#         children = db.query(Permission).filter(Permission.parent_id == first_level.id).all()
#
#         if children:
#             # todo 将返回的结果添加到children下
#             first_menu["children"] = (get_children(db, children))
#         tree.append(first_menu)
#
#     return tree
#
#
# # 递归获取所有的子解点，无限递归
# def get_children(db: Session, children: [Permission]):
#     son_children = []
#
#     for child in children:
#         next_menu = {
#             "id": child.id,
#             "label": child.name,
#             "children": []
#         }
#
#         next_children = db.query(Permission).filter(Permission.parent_id == child.id).all()
#
#         if next_children:
#             next_menu["children"] = (get_children(db, next_children))
#
#         son_children.append(next_menu)
#
#     return son_children
#
#
# # 根据role_id获取所有的权限id：权限id列表
# def get_permission_ids_by_role_id(db: Session, role_id: int):
#     perms = db.query(RolePermissions.perm_id).filter(RolePermissions.role_id == role_id).all()
#     perm_ids = []
#     for perm in perms:
#         perm_ids.append(perm.perm_id)
#
#     return perm_ids
#
#
# # 角色绑定权限
# def add_role_perms(db: Session, id: int, perms: [str]):
#     role_perms_dels = db.query(RolePermissions).filter(RolePermissions.role_id == id).all()
#     if role_perms_dels:
#         for role_perms_del in role_perms_dels:
#             db.delete(role_perms_del)
#
#     role_perms_add = []
#     if perms:
#         for perm in perms:
#             role_user = RolePermissions(
#                 role_id=id,
#                 perm_id=perm,
#             )
#             role_perms_add.append(role_user)
#
#     db.add_all(role_perms_add)
#     db.commit()
#     db.flush()
#
#
# def get_role_id_by_user_id(db: Session, user_id: int):
#     tree = []
#
#     # 一个用户可以分配多个角色
#     role_users = db.query(RoleUsers.role_id).filter(RoleUsers.user_id == user_id).all()
#
#     for role_user in role_users:
#         role_id = role_user.role_id
#         role_perms = db.query(RolePermissions.perm_id).filter(RolePermissions.role_id == role_id).all()
#         for role_perm in role_perms:
#             perm_id = role_perm.perm_id
#             # 查一级菜单
#             first_level_perms = db.query(Permission).filter(Permission.id == perm_id, Permission.parent_id == 0).all()
#
#             for first_level in first_level_perms:
#                 if first_level.name == "首页":
#                     first_menu = {
#                         "icon": first_level.icon,
#                         "index": first_level.url,
#                         "title": first_level.name
#                     }
#                 else:
#                     first_menu = {
#                         "icon": first_level.icon,
#                         "index": first_level.url,
#                         "title": first_level.name,
#                         "subs": []
#                     }
#
#                 children = db.query(Permission).filter(Permission.parent_id == first_level.id).all()
#
#                 if children:
#                     # todo 将返回的结果添加到children下
#                     first_menu["subs"] = (get_menu_children(db, children))
#                 tree.append(first_menu)
#
#     return tree
#
#
# # 递归获取所有的子解点，无限递归
# def get_menu_children(db: Session, children: [Permission]):
#     son_children = []
#
#     for child in children:
#         next_menu = {
#             # "icon": child.icon,
#             "index": child.url,
#             "title": child.name,
#             "subs": []
#         }
#
#         next_children = db.query(Permission).filter(Permission.parent_id == child.id).all()
#
#         if next_children:
#             next_menu["subs"] = (get_menu_children(db, next_children))
#         else:
#             next_menu.pop("subs")
#
#         son_children.append(next_menu)
#
#     return son_children
