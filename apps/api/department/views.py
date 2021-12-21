from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from utils import token
from db.get_db import get_db
from models.department.department_ret import DepartmentRet
from utils.depatrment_operation import get_department_pagenation, \
    get_department_total, \
    department_update, \
    delete_department_by_id, \
    add_department, \
    query_department, \
    get_department_query_totle

router = APIRouter(
    prefix="/department"
)


@router.get("/department_list", tags=["部门模块"])
def get_department_list(page_size: int, current_page: int, id: str = Depends(token.parse_token),
                        db: Session = Depends(get_db)):
    """
    分页查询部门信息
    :param page_size:
    :param current_page:
    :param id:
    :param db:
    :return:
    """
    departments = get_department_pagenation(db, page_size, current_page)
    total = get_department_total(db)
    content = {
        "departments": departments,
        "pageSize": page_size,
        "pageTotal": total,
        "currentPage": current_page
    }
    return content


@router.post("/edit", tags=["部门模块"])
def edit(
        id: int = Form(...),
        name: str = Form(...),
        leader: str = Form(None),
        desc: str = Form(...),
        user_id: str = Depends(token.parse_token),
        db: Session = Depends(get_db)):
    """
    通过id，更改部门的信息
    :param id:
    :param name:
    :param leader:
    :param desc:
    :param user_id:
    :param db:
    :return:
    """
    department_update(db, id, name, leader, desc)
    return {"code": 200, "msg": "更新成功", "id": id}


@router.post("/delete", tags=["部门模块"])
def delete_department(department: DepartmentRet, user_id: str = Depends(token.parse_token),
                      db: Session = Depends(get_db)):
    """
    根据id，删除部门信息
    :param department:
    :param user_id:
    :param db:
    :return:
    """
    id = department.id
    delete_department_by_id(db, id)
    return JSONResponse(content={"code": 200, "msg": "删除成功", "id": id})


@router.post("/add", tags=["部门模块"])
def add(
        name: str = Form(...),
        leader: str = Form(None),
        desc: str = Form(...),
        user_id: str = Depends(token.parse_token),
        db: Session = Depends(get_db)):
    """
    增加部门信息
    :param name:
    :param leader:
    :param desc:
    :param user_id:
    :param db:
    :return:
    """
    add_department(db, name, leader, desc)
    return JSONResponse(content={"code": 200, "msg": "添加成功"})


# 查询
@router.get("/query", tags=["部门模块"])
def query(
        department_name: str,
        page_size: int,
        current_page: int,
        user_id: str = Depends(token.parse_token),
        db: Session = Depends(get_db)):
    """
    按照部门名称，查询部门信息
    :param department_name:
    :param page_size:
    :param current_page:
    :param user_id:
    :param db:
    :return:
    """
    if department_name == "" or department_name == None or department_name == '':
        departments = get_department_pagenation(db, page_size, current_page)
        total = get_department_total(db)
    else:
        department_name = department_name.strip()
        departments = query_department(db, department_name, page_size, current_page)
        total = get_department_query_totle(db, department_name)

    content = {
        "departments": departments,
        "pageSize": page_size,
        "pageTotal": total,
        "currentPage": current_page
    }
    return content
