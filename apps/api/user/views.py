from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from utils import token
from db.get_db import get_db
from utils.user_operation import \
    get_user_pagenation, \
    get_user_total, \
    active, get_departments, user_update, \
    delete_user_by_id, \
    add_user, \
    query_user, \
    get_user_query_totle, \
    get_query_user_pagenation, \
    get_query_user_total, \
    get_no_departments

from models.user.user_ret_model import UserRet
from fastapi.responses import JSONResponse
from utils.get_md5_data import get_md5_pwd

router = APIRouter(
    prefix="/user"
)


@router.get("/user_list", tags=["用户模块"])
def get_user_list(page_size: int, current_page: int, id: str = Depends(token.parse_token),
                  db: Session = Depends(get_db)):
    """
    分页查询用户所有数据
    :param page_size: 当前查询显示几个值出来
    :param current_page: 当前页码
    :param id:  用户id
    :param db:
    :return:
    """
    users = get_user_pagenation(db, page_size, current_page)
    total = get_user_total(db)
    departments = get_departments(db)
    content = {

        "departments": departments,
        "users": users,
        "pageSize": page_size,  # 当前页面显示几个数据
        "pageTotal": total,  # 符合条件的总数
        "currentPage": current_page  # 当前页码
    }
    return content


@router.post("/active", tags=["用户模块"])
def active_user(user: UserRet, id: str = Depends(token.parse_token), db: Session = Depends(get_db)):
    """
    根据用户id，修改用户是否启用
    :param user:
    :param id:
    :param db:
    :return:
    """
    state = 1
    if user.state == 1:  # 正在启用
        state = 2  # 前端显示停用按钮
    if user.state == 2:  # 正在停用
        state = 1

    active(db, user.id, state)

    if user.state == 1:  # 正在启用
        return {"code": 200, "msg": "停用成功", "state": 2}
    if user.state == 2:  # 正在停用
        return {"code": 200, "msg": "启用成功", "state": 1}


@router.post("/edit", tags=["用户模块"])
async def edit(
        avatar: UploadFile = File(...),
        id: int = Form(...),
        username: str = Form(...),
        pwd: str = Form(None),
        addr: str = Form(...),
        department_name: str = Form(...),  # 通过部门名称，从数据库查找部门id，然后在数据库进行修改
        state: int = Form(...),
        user_id: str = Depends(token.parse_token),
        db: Session = Depends(get_db)):
    """
    图片上传必须使用formdata的模式
    :param avatar: 图片的路径
    :param id: 用户id
    :param username:用户名
    :param pwd: 密码
    :param addr: 地址
    :param department_name: 部门名称
    :param state: 当前是否启用
    :param user_id:
    :param db:
    :return:
    """
    rep = await avatar.read()
    file_path = "static/users/" + avatar.filename  # fastapi里面对路径是相对项目的
    with open(file_path, "wb") as f:
        f.write(rep)
    # 密码修改
    if pwd:
        md5_pwd = get_md5_pwd(pwd)
    else:
        md5_pwd = None
    # 数据库更新
    resp = user_update(db, id, username, md5_pwd, addr, state, file_path, department_name)
    if resp == 'successful':
        return {"code": 200, "msg": "更新成功", "id": id}
    else:
        return {"code": 500, "msg": "用户已删除，请联系管理员", "id": id}


@router.post("/delete", tags=["用户模块"])
def delete_user(user: UserRet, user_id: str = Depends(token.parse_token),
                db: Session = Depends(get_db)):
    """
    根据id，删除用户数据
    :param user:
    :param user_id:
    :param db:
    :return:
    """
    id = user.id
    delete_user_by_id(db, id)
    return JSONResponse(content={"code": 200, "msg": "删除成功", "id": id})


@router.post("/add", tags=["用户模块"])
async def add(
        avatar: UploadFile = File(...),
        username: str = Form(...),
        pwd: str = Form(None),
        addr: str = Form(...),
        state: int = Form(...),
        department_name: str = Form(...),
        user_id: str = Depends(token.parse_token),
        db: Session = Depends(get_db)):
    """
    设计到增加图片，要使用formdata模式
    :param avatar:
    :param username:
    :param pwd:
    :param addr:
    :param state:
    :param department_name:
    :param user_id:
    :param db:
    :return:
    """
    if avatar:
        rep = await avatar.read()
        file_path = "static/users/" + avatar.filename
        with open(file_path, "wb") as f:
            f.write(rep)

    md5_pwd = get_md5_pwd(pwd)
    add_user(db, username, md5_pwd, file_path, department_name, addr, state)

    return JSONResponse(content={"code": 200, "msg": "添加成功"})


@router.get("/query", tags=["用户模块"])
def query(
        username: str = "",
        department_name: str = "",
        page_size: int = 0,
        current_page: int = 0,
        user_id: str = Depends(token.parse_token),
        db: Session = Depends(get_db)):
    """
    带有分页效果的查询
    通过部门和用户名，来进行查询
    :param username:    查询的用户名
    :param department_name: 部门名称
    :param page_size: 当前查询显示几个值出来
    :param current_page: 当前页码
    :param user_id: 用户id
    :param db:
    :return:
    """
    if username == "" or username == None or username == '':
        users = get_query_user_pagenation(db, page_size, current_page, department_name)
        # 查询符合当前条件数据的总数
        total = get_query_user_total(db, department_name)

    else:
        username = username.strip()
        users = query_user(db, username, page_size, current_page, department_name)
        # 查询符合当前条件数据的总数
        total = get_user_query_totle(db, username, department_name)

    content = {
        "users": users,  # 查询到的user信息
        "pageSize": page_size,  # 当前页面显示几个数据
        "pageTotal": total,  # 符合条件的总数
        "currentPage": current_page  # 当前页码
    }
    return content


@router.get("/get_departments", tags=["用户模块"])
def get_department_datas(user_id: str = Depends(token.parse_token),
                         db: Session = Depends(get_db)):
    """
    获取所有的部门，增加用户信息的时候用
    :param user_id:
    :param db:
    :return:
    """
    departments = get_departments(db)
    return {"code": 200, "msg": "查询成功", "departments": departments}


@router.get("/get_no_departments", tags=["用户模块"])
def get_no_department_datas(id: int, user_id: str = Depends(token.parse_token),
                            db: Session = Depends(get_db)):
    """
    获取除了用户本身所在以外的所有部门，修改用户信息的时候用
    :param id:
    :param user_id:
    :param db:
    :return:
    """
    departments = get_no_departments(db, id)

    return {"code": 200, "msg": "查询成功", "departments": departments}
