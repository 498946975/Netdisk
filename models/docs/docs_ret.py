from pydantic import BaseModel
from typing import Optional


class DocsRet(BaseModel):
    id: Optional[int]
    # 文件夹或者文件名称
    name: Optional[str]
    # 文件夹和文件的表示，1：文件夹，2：文件
    flag: Optional[int]
    # 父级文件夹id，没有父级则为0
    pid: Optional[int]
    # 文件存放路径
    filepath: Optional[str]
    # 文件类型
    filetype: Optional[str]
    # 用户外键
    user_id: Optional[int]
    # 原文件名称
    resouce_name: Optional[str]
    # 创建时间: 年月日 时分秒
    create_time: Optional[str]
    # 创建日期：年月日
    create_date: Optional[str]
