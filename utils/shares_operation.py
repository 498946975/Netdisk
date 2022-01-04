import datetime
from sqlalchemy.orm import Session
from models.shares.shares_model import Shares, ShareItem
from models.docs.docs_model import Docs


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


def share_db_varify(db: Session, share_url: str, share_pwd: str) -> Shares:
    """
    校验url和提取码
    :param db:
    :param share_url:
    :param share_pwd:
    :return:
    """
    share: Shares = db.query(Shares).filter(Shares.share_url == share_url, Shares.share_pwd == share_pwd).first()
    return share


def get_share_docs_pagenation(db: Session, page_size: int, current_page: int, share_id: int) -> [Docs]:
    """
    通过share_id，拿到分享的docs
    :param db:
    :param page_size:
    :param current_page:
    :param share_id:
    :return:
    """
    share: Shares = db.query(Shares).filter(Shares.id == share_id).first()
    # 表示有人数限制，access_type=1的时候不判断
    if share.access_type == 2 and share.access_number <= 0:
        docs = []
    elif share.share_type != 1:  # 表示有过期时间
        now_time = datetime.datetime.now()
        if now_time > share.end_time:  # 当前时间大于endtime表示已过期
            docs = []
        else:
            # 根据share_id和docs的对应关系，返回分享的docs列表
            docs = db.query(ShareItem.doc_id).filter(ShareItem.share_id == share.id).all()
            doc_ids = []
            for doc in docs:
                doc_ids.append(doc.doc_id)
            # 根据doc_ids,查询分享docs的信息
            docs = db.query(
                Docs.id,
                Docs.name,
                Docs.flag,
                Docs.pid,
                Docs.filepath,
                Docs.filetype,
                Docs.create_time
            ).filter(Docs.id.in_(doc_ids)).order_by(Docs.id.desc()).limit(page_size).offset(
                (current_page - 1) * page_size).all()
    else:
        docs = db.query(ShareItem.doc_id).filter(ShareItem.share_id == share.id).all()
        doc_ids = []
        for doc in docs:
            doc_ids.append(doc.doc_id)
        docs = db.query(
            Docs.id,
            Docs.name,
            Docs.flag,
            Docs.pid,
            Docs.filepath,
            Docs.filetype,
            Docs.create_time
        ).filter(Docs.id.in_(doc_ids)).order_by(Docs.id.desc()).limit(page_size).offset(
            (current_page - 1) * page_size).all()
    # 访问次数自减少
    if share.access_type == 2:
        if share.access_number > 0:
            share.access_number = share.access_number - 1
            db.commit()
            db.flush()
            db.refresh(share)
    return docs
