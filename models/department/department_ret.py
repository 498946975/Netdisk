'''
@IDE ：PyCharm
@Author ：知了-海龙
@Date ：2021/8/18 11:44
@Email：hallen200806@163.com
@Desc ：
'''

from pydantic import BaseModel
from typing import Optional


class DepartmentRet(BaseModel):
    id: Optional[int]
    # 部门名称
    name: Optional[str]
    # 部门主管
    leader: Optional[str]
    # 部门职责
    desc: Optional[str]
    # 创建时间
    create_time: Optional[str]
