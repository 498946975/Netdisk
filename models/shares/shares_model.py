from db.db import Base
from sqlalchemy import Column, Integer, String, DateTime, Date, ForeignKey
import datetime


class Shares(Base):
    __tablename__ = "shares"
    id = Column(Integer, primary_key=True, autoincrement=True)
    # 用户外键
    user_id = Column(Integer, ForeignKey("user.id"))
    # 分享的连接
    share_url = Column(String(255))
    # 分享的提取码
    share_pwd = Column(String(32))
    # 分享类型，是永久的，还是指定时间过期，1:永久，2:一个月,3:七天,4:一天
    share_type = Column(Integer)
    # 分享开始时间
    start_time = Column(DateTime, default=datetime.datetime.now)
    # 分享结束时间
    end_time = Column(DateTime, default=datetime.datetime.now)
    # 启用还是关闭分享,1:开启,2:关闭
    state = Column(Integer, default=1)
    # 访问人数，1：不限，2：具体人数
    access_type = Column(Integer)
    # 访问人数设置
    access_number = Column(Integer)
    # 创建时间: 年月日 时分秒
    create_time = Column(DateTime, default=datetime.datetime.now)
    # 创建日期：年月日
    create_date = Column(Date, default=datetime.datetime.now)


class ShareItem(Base):
    """
    连接和文件的对应关系
    1对多的关系
    1个链接，对应多个文件or文件夹
    """
    __tablename__ = "share_items"
    id = Column(Integer, primary_key=True, autoincrement=True)
    # 分享表外键
    share_id = Column(Integer, ForeignKey("shares.id"))
    # 文件夹或文件的外键
    doc_id = Column(Integer, ForeignKey("docs.id"))
