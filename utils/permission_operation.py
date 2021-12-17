from sqlalchemy.orm import Session
from models.permission.permission_model import Permission
import datetime


def get_permission_by_id(db: Session, id: int) -> Permission:
    """
    根据id，查询当前权限的信息
    :param db:
    :param id:
    :return:
    """
    permission = db.query(
        Permission.id,
        Permission.name,
        Permission.url,
        Permission.method,
        Permission.args,
        Permission.parent_id,
        Permission.desc,
        Permission.create_time
    ).filter(Permission.id == id).first()

    return permission


def get_permission_total(db: Session) -> int:
    """
    获取权限表的总数量
    :param db:
    :return:
    """
    total = db.query(Permission).count()
    return total


# SELECT * from `user` LIMIT (page-1)*pagesize,5
def get_permission_pagenation(db: Session, page_size: int, current_page: int) -> [Permission]:
    """
    权限表格的所有数据分页查询
    :param db:
    :param page_size:
    :param current_page:
    :return:
    """
    permissions = db.query(
        Permission.id,
        Permission.name,
        Permission.url,
        Permission.method,
        Permission.args,
        Permission.parent_id,
        Permission.desc,
        Permission.create_time
    ).limit(page_size).offset((current_page - 1) * page_size).all()
    return permissions


def delete_permission_by_id(db: Session, id: int):
    """
    根据权限id删除权限
    :param db:
    :param id:
    :return:
    """
    permission = db.query(Permission).filter(Permission.id == id).first()
    db.delete(permission)
    db.commit()
    db.flush()


def permission_update(db: Session, id: int, name: str, url: str, method: str, args: str, parent_name: str, desc: str,
                      icon: str):
    """
    权限编辑
    :param db:
    :param id:
    :param name:
    :param url:
    :param method:
    :param args:
    :param parent_name:
    :param desc:
    :param icon:
    :return:
    """
    permission = db.query(Permission).filter(Permission.id == id).first()
    permission.name = name
    permission.url = url
    permission.method = method
    permission.args = args
    permission.desc = desc
    permission.icon = icon

    if parent_name != "无":  # 表示编辑候得结果一个一级菜单
        p = db.query(Permission).filter(Permission.name == parent_name).first()
        # 选择父级别菜单的名称，返回父级别的id号，赋值给当前权限
        permission.parent_id = p.id
    db.commit()
    db.flush()


def get_no_parent_names(db: Session, id: int) -> []:
    """
    拿到除自身父级别菜单的，所有父级别菜单
    :param db:
    :param id:
    :return:
    """
    has_permission: Permission = db.query(Permission).filter(Permission.id == id).first()
    # has_permission.parent_id == 0表示是一级菜单
    if has_permission.parent_id == 0:
        # 是一级菜单,剔除自身
        no_parents = db.query(Permission).filter(Permission.id != has_permission.id).all()
    else:
        # 是二级菜单，本身拥有的一级菜单要去出
        # 是二级菜单，需要弹出除自身意外的所有级别
        ### 是二级菜单，parent_id和Permission.id是有关联的
        no_parents = db.query(Permission).filter(Permission.id != has_permission.parent_id).all()
    return no_parents


def add_permission(db: Session, name: str, url: str, method: str, args: str, parent_name: str, desc: str, icon: str):
    """
    增加权限信息
    :param db:
    :param name:
    :param url:
    :param method:
    :param args:
    :param parent_name:
    :param desc:
    :param icon:
    :return:
    """
    if parent_name == "无":
        parent_id = 0
    else:
        # 如果不是一级菜单，需要选择父级别的名称
        parent: Permission = db.query(Permission).filter(Permission.name == parent_name).first()
        # 通过父级别的名称，查询父级别的id，赋值给现在的权限
        parent_id = parent.id
    permission = Permission(
        name=name,
        url=url,
        method=method,
        args=args,
        desc=desc,
        icon=icon,
        parent_id=parent_id

    )
    db.add(permission)
    db.commit()
    db.flush()


def get_all_parent_info(db: Session) -> [Permission]:
    """
    获取所有的权限名称
    :param db:
    :return:
    """
    parents = db.query(Permission).all()
    return parents


