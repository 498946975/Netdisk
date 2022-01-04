from sqlalchemy.orm import Session
from models.docs.docs_model import Docs
from utils.get_random import get_random_num, get_timestemp


def get_doc_by_id(db: Session, doc_id: int) -> Docs:
    """
    通过文件id，拿到文件的信息
    :param db:
    :param doc_id:
    :return:
    """
    doc = db.query(Docs).filter(Docs.id == doc_id).first()
    return doc


def get_docs_by_ids(db: Session, ids: [str]):
    docs = db.query(Docs).filter(Docs.id.in_(ids)).all()
    name = ""
    path = ""
    for doc in docs:
        if doc.pid != 0:
            doc = db.query(Docs).filter(Docs.id == doc.pid).first()
            name = doc.name
            path = doc.filepath
        else:
            name = get_random_num(12) + "-" + get_timestemp()
            path = "uploads/docs/"

    return (docs, name, path)
