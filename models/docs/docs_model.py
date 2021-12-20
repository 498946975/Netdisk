from db.db import Base
from sqlalchemy import Column, Integer, String, DateTime, Date, ForeignKey
import datetime


class Docs(Base):
    __tablename__ = "docs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    # 文件夹或者文件名称
    name = Column(String(255), unique=True)
    # 文件夹和文件的表示，1：文件夹，2：文件
    flag = Column(Integer)
    # 父级文件夹id，没有父级则为0
    pid = Column(Integer)
    # 文件存放路径
    filepath = Column(String(255))
    # 文件类型
    filetype = Column(String(64))
    # 用户外键
    user_id = Column(Integer, ForeignKey("user.id"))
    # 原文件名称
    resouce_name = Column(String(255))
    # 创建时间: 年月日 时分秒
    create_time = Column(DateTime, default=datetime.datetime.now)
    # 创建日期：年月日
    create_date = Column(Date, default=datetime.datetime.now)
