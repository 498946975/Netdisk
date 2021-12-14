from sqlalchemy.orm import Session
from models.user.user_model import Department


def get_department_by_id(db: Session, id: int) -> Department:
    """
    根据id获取部门信息
    :param db:
    :param id:
    :return:
    """
    department = db.query(Department.id, Department.name, Department.leader, Department.desc,
                          Department.create_time).filter(Department.id == id).first()

    return department


# SELECT * from `user` LIMIT (page-1)*pagesize,5
def get_department_pagenation(db: Session, page_size: int, current_page: int) -> [Department]:
    """
    分页查询部门数据
    :param db:
    :param page_size:
    :param current_page:
    :return:
    """
    departments = db.query(
        Department.id,
        Department.name,
        Department.leader,
        Department.desc,
        Department.create_time
    ).limit(page_size).offset((current_page - 1) * page_size).all()
    return departments


def get_department_total(db: Session) -> int:
    """
    获取部门的总个数
    :param db:
    :return:
    """
    total = db.query(Department).count()
    return total


# 部门编辑
def department_update(db: Session, id: int, name: str, leader: str, desc: str):
    """
    编辑部门的资料
    :param db:
    :param id: id
    :param name: 部门名称
    :param leader: 部门领导
    :param desc: 部门描述
    :return:
    """
    department = db.query(Department).filter(Department.id == id).first()
    department.name = name
    department.leader = leader
    department.desc = desc

    db.commit()
    db.flush()


def delete_department_by_id(db: Session, id: int):
    """
    根据id删除部门（硬删除）
    :param db:
    :param id:
    :return:
    """
    department = db.query(Department).filter(Department.id == id).first()
    db.delete(department)
    db.commit()
    db.flush()


def add_department(db: Session, name: str, leader: str, desc: str):
    """
    增加部门信息
    :param db:
    :param name: 部门名称
    :param leader: 部门领导
    :param desc: 部门描述
    :return:
    """
    department = Department(
        name=name,
        leader=leader,
        desc=desc,

    )
    db.add(department)
    db.commit()
    db.flush()


def query_department(db: Session, department_name: str, page_size: int, current_page: int) -> [Department]:
    """
    根据部门名称，分页查询查询部门信息
    :param db:
    :param department_name:
    :param page_size:
    :param current_page:
    :return:
    """
    departments = db.query(
        Department.id,
        Department.name,
        Department.leader,
        Department.desc,
        Department.create_time
    ).filter(Department.name.like('%' + department_name + '%')).limit(page_size).offset((current_page - 1) * page_size).all()
    return departments


def get_department_query_totle(db: Session, department_name: str) -> int:
    """
    根据部门名称，统计有多少个相同名称的部门
    :param db:
    :param department_name:
    :return:
    """
    total = db.query(Department).filter(Department.name.like('%' + department_name + '%')).count()
    return total
