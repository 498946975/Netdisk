from db.db import Base
from sqlalchemy import Column, Integer, String, DateTime, Date, ForeignKey
import datetime
from sqlalchemy.orm import relationship


# 创建部门名称的表格模型，一定要放在User模型前面，因为User模型用到了这个部门表的外键
class Department(Base):
    __tablename__ = "department"
    id = Column(Integer, primary_key=True, autoincrement=True)
    # 部门名称
    name = Column(String(255), unique=True)
    # 部门主管
    leader = Column(String(255))
    # 部门职责
    desc = Column(String(255))
    # 用户表的反向关系：表的模型是User
    user = relationship("User", backref="department")
    # 创建时间: 年月日 时分秒
    create_time = Column(DateTime, default=datetime.datetime.now)
    # 创建日期：年月日
    create_date = Column(Date, default=datetime.datetime.now)


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    # 用户名
    username = Column(String(255))
    # 密码
    pwd = Column(String(255))
    # todo 部门外键
    dep_id = Column(Integer, ForeignKey('department.id'))
    # 头像
    avatar = Column(String(255), default="/static/users/img.jpg")
    # 地址
    addr = Column(String(255))
    # 状态,1表示启用，2表示停用
    state = Column(Integer, default=1)
    # 上次登录日期
    last_login_date = Column(Date, default=datetime.datetime.now)
    # 上次登录的IP地址
    ip = Column(String(255))
    # 逻辑删除，0 表示未删除，1表示已删除
    is_delete = Column(Integer, default=0)
    # 创建时间: 年月日 时分秒
    create_time = Column(DateTime, default=datetime.datetime.now)
    # 创建日期：年月日
    create_date = Column(Date, default=datetime.datetime.now)
