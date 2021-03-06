from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session
from utils import token
from db.get_db import get_db
from utils.download_operation import get_doc_by_id, get_docs_by_ids
from utils.zip_operation import zip_dir, zip_file_or_dir

router = APIRouter(
    prefix="/download"
)


@router.get("/shares_download", tags=["下载模块"])
def shares_download(
        doc_id: int,
        share_id: str = Depends(token.parse_token),
        db: Session = Depends(get_db)):
    """
    单个文件下载+单个文件夹下载
    :param doc_id:
    :param share_id:
    :param db:
    :return:
    """
    doc = get_doc_by_id(db, doc_id)
    # 单文件下载
    if doc.flag == 2:  # 文件，直接返回路径
        return {"code": 200, "msg": "查询成功", "filepath": doc.filepath}
    elif doc.flag == 1:  # 文件夹，打包后返回打包后的路径
        output_file = doc.filepath.rsplit("/", 1)[0] + "/" + doc.name + ".zip"
        dir = doc.filepath
        zip_dir(output_file, dir)
        return {"code": 200, "msg": "查询成功", "filepath": output_file}
    else:  # 直接返回错误信息，该文件丢失了
        return {"code": 500, "msg": "该文件丢失了"}


@router.get("/shares_downloads", tags=["下载模块"])
def shares_downloads(
        doc_ids: str,
        share_id: str = Depends(token.parse_token),
        db: Session = Depends(get_db)):
    """
    多文件下载
    :param doc_ids:
    :param share_id:
    :param db:
    :return:
    """
    doc_ids = doc_ids.split(",")
    docs, pname, path = get_docs_by_ids(db, doc_ids)
    output_file = path.rsplit("/", 1)[0] + "/" + pname + ".zip"
    zip_file_or_dir(db, output_file, docs)
    return {"code": 200, "msg": "下载成功", "filepath": output_file}
