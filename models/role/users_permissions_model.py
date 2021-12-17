from db.db import Base
from sqlalchemy import Column, Integer, DateTime, Date, ForeignKey
import datetime


class RolePermissions(Base):
    """
    中间表
    角色和权限的多对多关系
    """
    __tablename__ = "role_permissions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    # 角色外键
    role_id = Column(Integer, ForeignKey('role.id'))
    # 权限外键
    perm_id = Column(Integer, ForeignKey('permission.id'))
    # 创建时间: 年月日 时分秒
    create_time = Column(DateTime, default=datetime.datetime.now)
    # 创建日期：年月日
    create_date = Column(Date, default=datetime.datetime.now)


class RoleUsers(Base):
    """
    中间表
    角色和用户的多对多关系
    """
    __tablename__ = "role_users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    # 角色外键
    role_id = Column(Integer, ForeignKey('role.id'))
    # 用户外键
    user_id = Column(Integer, ForeignKey('user.id'))
    # 创建时间: 年月日 时分秒
    create_time = Column(DateTime, default=datetime.datetime.now)
    # 创建日期：年月日
    create_date = Column(Date, default=datetime.datetime.now)
