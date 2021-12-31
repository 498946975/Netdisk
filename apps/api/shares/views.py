import datetime
from fastapi import APIRouter, Depends, Form, UploadFile, File
from utils import token
from utils.get_share import get_share_random_str
from db.get_db import get_db
from utils.docs_operation import *
from utils.shares_operation import share_db_add, share_db_adds

router = APIRouter(
    prefix="/shares"
)


@router.post("/share_add", tags=["分享操作"])
def share_add(
        sharePwd: str = Form(None),
        share_type: int = Form(...),
        doc_id: int = Form(...),
        access_type: int = Form(...),
        access_number: int = Form(...),
        user_id: str = Depends(token.parse_token),
        db: Session = Depends(get_db)):
    """
    文件or文件夹，单独分享
    :param sharePwd: 提取码
    :param share_type: 分享类型，是永久的，还是指定时间过期，1:永久，2:一个月,3:七天,4:一天
    :param doc_id:  文档id
    :param access_type:  访问人数，1：不限，2：具体人数
    :param access_number:  访问人数具体设置
    :param user_id:
    :param db:
    :return:
    """
    # 生成随机字符串
    share_url = get_share_random_str(16)
    # share_pwd进行判断，如果为空则自动生成，否则直接使用
    if sharePwd == None or sharePwd == "":
        sharePwd = get_share_random_str(4)
    # 根据有效期判断，传开始时间和结束时间
    end_time = datetime.datetime.now()
    # 访问人数设置
    if access_type == 1:
        access_number = 0
    elif access_type == 2:
        access_number = access_number
    else:
        access_number = 0
    # 访问时间设置
    if share_type != 1:
        if share_type == 2:
            now_time = datetime.datetime.now()
            end_time = now_time + datetime.timedelta(days=30)
        if share_type == 3:
            now_time = datetime.datetime.now()
            end_time = now_time + datetime.timedelta(days=7)
        if share_type == 4:
            now_time = datetime.datetime.now()
            end_time = now_time + datetime.timedelta(days=1)
    elif share_type == 1:
        now_time = datetime.datetime.now()
        end_time = now_time + datetime.timedelta(days=99999)
    # 访问状态设置
    state = 1
    share_db_add(
        db, int(user_id),
        share_url, sharePwd,
        share_type, end_time,
        state, access_type, access_number,
        doc_id
    )
    return {"code": 200, "msg": "分享成功", "share_url": share_url, "share_pwd": sharePwd}


@router.post("/share_adds", tags=["文档模块"])
def share_adds(
        sharePwd: str = Form(None),
        share_type: int = Form(...),
        doc_ids: str = Form(...),
        access_type: int = Form(...),
        access_number: int = Form(...),
        user_id: str = Depends(token.parse_token),
        db: Session = Depends(get_db)):
    """
    多选文件分享
    :param sharePwd:
    :param share_type:
    :param doc_ids:
    :param access_type:
    :param access_number:
    :param user_id:
    :param db:
    :return:
    """
    doc_ids = doc_ids.split(",")
    # 生成随机字符串
    share_url = get_share_random_str(16)
    # share_pwd进行判断，如果为空则自动生成，否则直接使用
    if sharePwd == None or sharePwd == "":
        sharePwd = get_share_random_str(4)

    # todo 根据有效期判断，传开始时间和结束时间
    end_time = datetime.datetime.now()

    # 访问人数设置
    if access_type == 1:
        access_number = 0
    elif access_type == 2:
        access_number = access_number
    else:
        access_number = 0
    if share_type != 1:
        if share_type == 2:
            now_time = datetime.datetime.now()
            end_time = now_time + datetime.timedelta(days=30)
        if share_type == 3:
            now_time = datetime.datetime.now()
            end_time = now_time + datetime.timedelta(days=7)
        if share_type == 4:
            now_time = datetime.datetime.now()
            end_time = now_time + datetime.timedelta(days=1)
    elif share_type == 1:
        now_time = datetime.datetime.now()
        end_time = now_time + datetime.timedelta(days=99999)

    state = 1
    share_db_adds(
        db, int(user_id),
        share_url, sharePwd,
        share_type, end_time,
        state, access_type, access_number,
        doc_ids
    )

    return {"code": 200, "msg": "分享成功", "share_url": share_url, "share_pwd": sharePwd}
