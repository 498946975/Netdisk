from fastapi import APIRouter, Depends, Form, UploadFile, File
from utils import token
from utils.create_dir import create_dir
from db.get_db import get_db
from utils.docs_operation import *
from fastapi.responses import JSONResponse
from models.docs.docs_ret import DocsRet
from utils.get_random import get_random_num, get_timestemp


router = APIRouter(
    prefix="/docs"
)


@router.get("/doc_list", tags=["文档模块"])
def get_doc_list(pid: int, flag: int, page_size: int, current_page: int, id: str = Depends(token.parse_token),
                 db: Session = Depends(get_db)):
    """
    文档列表首页，分页查询出所有的一级目录
    :param pid:
    :param flag:
    :param page_size:
    :param current_page:
    :param id:
    :param db:
    :return:
    """
    docs = get_doc_pagenation(db, page_size, current_page, pid, flag)
    total = get_doc_total(db, pid, flag)
    content = {
        "docs": docs,
        "pageSize": page_size,
        "pageTotal": total,
        "currentPage": current_page
    }
    return content


@router.post("/edit", tags=["文档模块"])
def edit(
        id: int = Form(...),
        name: str = Form(...),
        user_id: str = Depends(token.parse_token),
        db: Session = Depends(get_db)):
    """
    根据id，修改一级文件夹名称
    :param id:
    :param name:
    :param user_id:
    :param db:
    :return:
    """
    doc_update(db, id, name)
    return {"code": 200, "msg": "更新成功", "id": id}


@router.post("/delete", tags=["文档模块"])
def delete_doc(docs: DocsRet, user_id: str = Depends(token.parse_token),
               db: Session = Depends(get_db)):
    """
    根据id，删除文件夹，或者文件名称
    :param docs:
    :param user_id:
    :param db:
    :return:
    """
    # todo 需要做软删除，需要重新构建models，增加软删除的字段
    id = docs.id
    delete_doc_by_id(db, id)
    return JSONResponse(content={"code": 200, "msg": "删除成功", "id": id})


@router.get("/query", tags=["文档模块"])
def query(
        input_name: str,
        page_size: int,
        current_page: int,
        pid: int,
        flag: int,
        user_id: str = Depends(token.parse_token),
        db: Session = Depends(get_db)):
    """
    根据输入的名称，搜索文件or文件夹
    :param input_name:
    :param page_size:
    :param current_page:
    :param pid:
    :param flag:
    :param user_id:
    :param db:
    :return:
    """
    input_name = input_name.strip()
    docs = query_docs(db, input_name, page_size, current_page, pid, flag)
    total = get_docs_query_totle(db, input_name, pid, flag)

    content = {
        "docs": docs,
        "pageSize": page_size,
        "pageTotal": total,
        "currentPage": current_page
    }
    return content


@router.post("/add_folder", tags=["文档模块"])
def add(
        name: str = Form(...),
        pid: int = Form(...),
        user_id: str = Depends(token.parse_token),
        db: Session = Depends(get_db)):
    """
    增加一级文件夹
    :param name:
    :param pid:
    :param user_id:
    :param db:
    :return:
    """
    docs = get_doc_by_name(db, name)
    if docs:
        return JSONResponse(content={"code": 500, "msg": "该文件夹已存在，请重新输入"})

    base_dir = "uploads/docs/"
    if pid == 0:  # 一级文件夹
        path = base_dir + name
        create_dir(path)
    else:
        name_list = get_pname_by_pid(db, pid)
        # 例如name_list = ["四级文件夹", "三级文件夹", "二级文件夹", "一级文件夹", ]
        # reversed的作用是反转一下，变为["一级文件夹", "二级文件夹", "三级文件夹", "四级文件夹", ]
        new_name_list = list(reversed(name_list))
        new_name_list = "/".join(new_name_list)
        path = base_dir + new_name_list + "/" + name
        create_dir(path)

    add_docs(db, name, int(user_id), pid, path)

    return JSONResponse(content={"code": 200, "msg": "添加成功"})


@router.post("/upload_files", tags=["文档模块"])
async def upload(
        file: UploadFile = File(...),
        pid: int = Form(...),
        flag: int = File(...),
        user_id: str = Depends(token.parse_token),
        db: Session = Depends(get_db)):
    """
    上传文件
    :param file:
    :param pid:
    :param flag:
    :param user_id:
    :param db:
    :return:
    """
    if pid == 0 and flag == 2:
        return {"code": 500, "msg": "不允许在根目录下上传文件"}
    rep = await file.read()
    # 文件名称可能会重复:12个随机数+时间戳
    new_prefix = get_random_num(12) + "-" + get_timestemp()
    new_name = new_prefix + "-" + file.filename
    file_path = get_path_by_pid(db, pid) + "/" + new_name
    # 上传文件到网盘
    with open(file_path, "wb") as f:
        f.write(rep)
    # 文件后缀
    file_type = file.filename.rsplit(".", 1)[1]
    # 将文件基础信息，存入数据库
    save_upload(db, new_name, pid, flag, file_path, file_type, int(user_id), file.filename)
    return {"code": 200, "msg": "上传成功"}
