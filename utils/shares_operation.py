import datetime
from sqlalchemy.orm import Session
from models.shares.shares_model import Shares, ShareItem


def share_db_add(
        db: Session,
        user_id: int,
        share_url: str,
        share_pwd: str,
        share_type: int,
        end_time: datetime.datetime,
        state: int,
        access_type: int,
        access_number: int,
        doc_id: int
):
    """
    增加单独文件分享
    :param db:
    :param user_id:
    :param share_url:
    :param share_pwd:
    :param share_type:
    :param end_time:
    :param state:
    :param access_type:
    :param access_number:
    :param doc_id:
    :return:
    """
    share = Shares(
        user_id=user_id,
        share_url=share_url,
        share_pwd=share_pwd,
        share_type=share_type,
        end_time=end_time,
        state=state,
        access_type=access_type,
        access_number=access_number,
    )
    # 单独文件分享增加到数据库
    db.add(share)
    db.commit()
    db.flush()
    # 分享到id和文件id进行关联
    share_item = ShareItem(
        share_id=share.id,
        doc_id=doc_id
    )
    db.add(share_item)
    db.commit()
    db.flush()


def share_db_adds(
        db: Session,
        user_id: int,
        share_url: str,
        share_pwd: str,
        share_type: int,
        end_time: datetime.datetime,
        state: int,
        access_type: int,
        access_number: int,
        doc_ids: [str]
):
    """
    多条分享
    :param db:
    :param user_id:
    :param share_url:
    :param share_pwd:
    :param share_type:
    :param end_time:
    :param state:
    :param access_type:
    :param access_number:
    :param doc_ids:
    :return:
    """
    share = Shares(
        user_id=user_id,
        share_url=share_url,
        share_pwd=share_pwd,
        share_type=share_type,
        end_time=end_time,
        state=state,
        access_type=access_type,
        access_number=access_number,
    )
    db.add(share)
    db.commit()
    db.flush()
    # 保存多条分享的映射关系
    for doc_id in doc_ids:
        share_item = ShareItem(
            share_id=share.id,
            doc_id=doc_id
        )
        db.add(share_item)

    db.commit()
    db.flush()
