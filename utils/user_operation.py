import datetime
from sqlalchemy.orm import Session
from models.user.user_model import User, Department


def get_user_by_username_and_pwd(db: Session, username: str, md5_pwd: str) -> User:
    """
    根据用户名密码，查询数据库，返回用户除密码外的全部信息
    :param db:
    :param username: 用户名
    :param md5_pwd: 密码
    :return:
    """
    user = db.query(User.id, User.username, User.avatar, User.ip, User.last_login_date, User.state,
                    User.is_delete).filter(
        User.username == username, User.pwd == md5_pwd).first()
    return user


def get_user_by_id(db: Session, id: int) -> User:
    """
    根据id，返回除密码外的，所有用户信息
    :param db:
    :param id:
    :return:
    """
    user = db.query(
        User.id,
        User.username,
        User.avatar,
        User.ip,
        User.last_login_date,
        User.dep_id,
        User.state,
        User.addr,
        Department.name
    ).join(Department).filter(User.id == id).first()

    return user


# 分页
# SELECT * from `user` LIMIT (page-1)*pagesize,5
def get_user_pagenation(db: Session, page_size: int, current_page: int) -> [User]:
    """
    分页查询
    :param db:
    :param page_size:
    :param current_page:
    :return:
    """
    users = db.query(
        User.id,
        User.username,
        User.avatar,
        User.addr,
        User.state,
        User.ip,
        User.last_login_date,
        User.create_time,
        User.dep_id,
        Department.name
    ).join(Department).limit(page_size).offset((current_page - 1) * page_size).all()
    # join：关联查询
    # limit：每页显示多少条数据
    # offset：偏移量
    return users


# 获取总数量
def get_user_total(db: Session) -> int:
    """
    获取所有用户总数
    :param db:
    :return:
    """
    total = db.query(User).count()
    return total


def active(db: Session, id: int, state: int):
    """
    用户启用停用提交到数据库
    :param db:
    :param id:
    :param state:
    :return:
    """
    user = db.query(User).filter(User.id == id).first()
    user.state = state
    db.commit()
    db.flush()


# 用户编辑
def user_update(db: Session, id: int, username: str, pwd: str, addr: str, state: int, avatar: str,
                department_name: str):
    """
    编辑用户资料
    :param db:
    :param id: 用户id
    :param username: 用户名
    :param pwd: 密码
    :param addr: 地址
    :param state: 用户状态
    :param avatar: 头像图片
    :param department_name: 部门名称
    :return:
    """
    # # 通过部门名称，从数据库查找部门id，然后在数据库进行修改
    department = db.query(Department).filter(Department.name == department_name).first()

    user = db.query(User).filter(User.id == id).first()
    # 判断用户是否软删除，0是没有删除，1是已经删除
    if user.is_delete == 0:
        user.username = username
        user.state = state
        user.addr = addr
        user.dep_id = department.id
        user.avatar = "/" + avatar
        if pwd:
            user.pwd = pwd
        db.commit()
        db.flush()
        return "successful"
    else:
        return "fail"


def delete_user_by_id(db: Session, id: int):
    """
    根据用户id删除用户
    :param db:
    :param id:
    :return:
    """
    user = db.query(User).filter(User.id == id).first()
    user.is_delete = 1
    db.commit()
    db.flush()


def update_time_and_ip(db: Session, user_id: int, login_date: datetime.datetime, ip: str):
    """
    更新登陆时间和登陆IP
    :param db:
    :param user_id: 用户id
    :param login_date: 获取的登陆时间
    :param ip: 获取的登陆ip
    :return:
    """
    user = db.query(User).filter(User.id == user_id).first()
    user.last_login_date = login_date
    user.ip = ip
    db.commit()
    db.flush()


def add_user(db: Session, username: str, pwd: str, avatar: str, department_name: str, addr: str, state: int):
    """
    增加用户信息
    :param db:
    :param username: 设置用户名
    :param pwd: 给默认密码
    :param avatar: 设置头像
    :param department_name: 设置部门名称
    :param addr: 设置地址
    :param state:   设置用户是否启用
    :return:
    """
    department = db.query(Department).filter(Department.name == department_name).first()
    user = User(
        username=username,
        pwd=pwd,
        avatar="/" + avatar,
        addr=addr,
        state=state,
        dep_id=department.id,
        is_delete=0  # 是否软删除，默认值给个0，不删除
    )

    db.add(user)
    db.commit()
    db.flush()


def query_user(db: Session, username: str, page_size: int, current_page: int, department_name: str) -> [User]:
    """
    给用户名，给部门名称，查询用户数据
    :param db:
    :param username:
    :param page_size:
    :param current_page:
    :param department_name:
    :return:
    """
    department = db.query(Department).filter(Department.name == department_name).first()

    if department:
        # 如果有部门的值，就按照部门和用户名，查询用户信息
        users = db.query(
            User.id,
            User.username,
            User.avatar,
            User.addr,
            User.state,
            User.ip,
            User.last_login_date,
            User.create_time,
            User.dep_id,
            Department.name
        ).filter(User.dep_id == department.id).join(Department).filter(User.username.like('%' + username + '%')).limit(
            page_size).offset((current_page - 1) * page_size).all()
    else:
        # 如果没有部门信息，就查询用户的所有的信息
        users = db.query(
            User.id,
            User.username,
            User.avatar,
            User.addr,
            User.state,
            User.ip,
            User.last_login_date,
            User.create_time,
            User.dep_id,
            Department.name
        ).join(Department).filter(User.username.like('%' + username + '%')).limit(page_size).offset(
            (current_page - 1) * page_size).all()
    return users


def get_user_query_totle(db: Session, username: str, department_name: str) -> int:
    """
    根据用户名和部门，获取符合条件的用户总数
    :param db:
    :param username:
    :param department_name:
    :return:
    """
    department = db.query(Department).filter(Department.name == department_name).first()

    if department:
        total = db.query(User).filter(User.username.like('%' + username + '%'), User.dep_id == department.id).count()
    else:
        total = db.query(User).filter(User.username.like('%' + username + '%')).count()
    return total


def get_query_user_pagenation(db: Session, page_size: int, current_page: int, department_name: str) -> [User]:
    """
    只根据部门信息，查询用户资料
    :param db:
    :param page_size:
    :param current_page:
    :param department_name:
    :return:
    """
    department = db.query(Department).filter(Department.name == department_name).first()

    if department:
        users = db.query(
            User.id,
            User.username,
            User.avatar,
            User.addr,
            User.state,
            User.ip,
            User.last_login_date,
            User.create_time,
            User.dep_id,
            Department.name
        ).filter(User.dep_id == department.id).join(Department).limit(page_size).offset(
            (current_page - 1) * page_size).all()
    else:
        users = db.query(
            User.id,
            User.username,
            User.avatar,
            User.addr,
            User.state,
            User.ip,
            User.last_login_date,
            User.create_time,
            User.dep_id,
            Department.name
        ).join(Department).limit(page_size).offset((current_page - 1) * page_size).all()
    return users


def get_query_user_total(db: Session, department_name: str) -> int:
    """
    按照部门，获取当前部门的用户总数
    :param db:
    :param department_name:
    :return:
    """
    department = db.query(Department).filter(Department.name == department_name).first()
    if department:
        total = db.query(User).filter(User.dep_id == department.id).count()
    else:
        total = db.query(User).count()
    return total


def get_departments(db: Session) -> [Department]:
    """
    获取部门的所有信息，增加用户信息的时候用到
    :param db:
    :return: 返回列表，部门id和名称
    """
    departments = db.query(Department.id, Department.name).all()
    return departments


def get_no_departments(db: Session, id: int) -> [Department]:
    """
    获取当前用户部门之外的所有部门，修改用户信息的时候用到
    :param db:
    :param id:
    :return:
    """
    user = db.query(User).filter(User.id == id).first()
    departments = db.query(Department.id, Department.name).filter(Department.id != user.dep_id).all()
    return departments
