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

    share_item = ShareItem(
        share_id=share.id,
        doc_id=doc_id
    )
    db.add(share_item)
    db.commit()
    db.flush()
