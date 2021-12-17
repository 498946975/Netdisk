from db.db import Base
from sqlalchemy import Column, Integer, String, DateTime, Date, ForeignKey
import datetime


class Permission(Base):
    __tablename__ = "permission"
    id = Column(Integer, primary_key=True, autoincrement=True)
    # 权限名称
    name = Column(String(255), unique=True)
    # url，前端的url
    url = Column(String(255))
    # 请求方法
    method = Column(String(255))
    # 参数
    args = Column(String(255))
    # 父級菜单id，如果是一级菜单则为0
    # 举例：用户管理是一级菜单（ID=0），用户列表是二级菜单（ID=1）
    parent_id = Column(Integer)
    # 描述
    desc = Column(String(255))
    # 菜单图标
    icon = Column(String(255))
    # 排序权重字段,数值越大排序越靠前
    sort = Column(Integer)
    # 创建时间: 年月日 时分秒
    create_time = Column(DateTime, default=datetime.datetime.now)
    # 创建日期：年月日
    create_date = Column(Date, default=datetime.datetime.now)
