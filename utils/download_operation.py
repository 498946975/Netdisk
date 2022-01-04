from sqlalchemy.orm import Session
from models.docs.docs_model import Docs


def get_doc_by_id(db:Session,doc_id:int) -> Docs:
    """
    通过文件id，拿到文件的信息
    :param db:
    :param doc_id:
    :return:
    """
    doc = db.query(Docs).filter(Docs.id == doc_id).first()
    return doc