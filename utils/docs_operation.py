from sqlalchemy.orm import Session
from models.docs.docs_model import Docs


def get_doc_pagenation(db: Session, page_size: int, current_page: int, pid: int, flag: int) -> [Docs]:
    """
    分页获取所有的
    :param db:
    :param page_size:
    :param current_page:
    :param pid:
    :param flag:
        flag=0，是查询文件和文件夹
        flag=1，是查询文件夹
        flag=2，是查询文件
    :return:
    """
    if flag == 0:
        docs = db.query(
            Docs.id,
            Docs.name,
            Docs.flag,
            Docs.pid,
            Docs.filepath,
            Docs.filetype,
            Docs.create_time
        ).filter(Docs.pid == pid).order_by(Docs.id.desc()).limit(page_size).offset(
            (current_page - 1) * page_size).all()

    elif flag == 1 or flag == 2:
        docs = db.query(
            Docs.id,
            Docs.name,
            Docs.flag,
            Docs.pid,
            Docs.filepath,
            Docs.filetype,
            Docs.create_time
        ).filter(Docs.pid == pid, Docs.flag == flag).order_by(Docs.id.desc()).limit(page_size).offset(
            (current_page - 1) * page_size).all()
    else:
        docs = []
    return docs


def get_doc_total(db: Session, pid: int, flag: int) -> int:
    """
    获取当前查询的总数
    :param db:
    :param pid:
    :param flag:
        flag=0，是查询文件和文件夹
        flag=1，是查询文件夹
        flag=2，是查询文件
    :return:
    """
    if flag == 0:
        total = db.query(Docs).filter(Docs.pid == pid).count()
    elif flag == 1 or flag == 2:
        total = db.query(Docs).filter(Docs.pid == pid, Docs.flag == flag).count()
    else:
        total = 0
    return total


def doc_update(db: Session, id: int, name: str):
    """
    更新文件or文件夹名称
    :param db:
    :param id:
    :param name:
    :return:
    """
    role = db.query(Docs).filter(Docs.id == id).first()
    role.name = name
    db.commit()
    db.flush()


def delete_doc_by_id(db: Session, id: int):
    """
    删除文件or文件夹
    :param db:
    :param id:
    :return:
    """
    doc = db.query(Docs).filter(Docs.id == id).first()
    db.delete(doc)
    db.commit()
    db.flush()


def query_docs(db: Session, input_name: str, page_size: int, current_page: int, pid: int, flag: int) -> [Docs]:
    """
    根据用户输入的内容，查询对应的文件or文件夹
    :param db:
    :param input_name:
    :param page_size:
    :param current_page:
    :param pid:
    :param flag:
        flag=0，是查询文件和文件夹
        flag=1，是查询文件夹
        flag=2，是查询文件
    :return:
    """
    if flag == 0:
        docs = db.query(
            Docs.id,
            Docs.name,
            Docs.flag,
            Docs.pid,
            Docs.filepath,
            Docs.filetype,
            Docs.create_time
        ).order_by(Docs.id.desc()).filter(Docs.name.like('%' + input_name + '%'), Docs.pid == pid).limit(
            page_size).offset(
            (current_page - 1) * page_size).all()
    elif flag == 1 or flag == 2:
        docs = db.query(
            Docs.id,
            Docs.name,
            Docs.flag,
            Docs.pid,
            Docs.filepath,
            Docs.filetype,
            Docs.create_time
        ).filter(Docs.name.like('%' + input_name + '%'), Docs.pid == pid, Docs.flag == flag).limit(page_size).offset(
            (current_page - 1) * page_size).all()
    else:
        docs = []
    return docs


def get_docs_query_totle(db: Session, input_name: str, pid: int, flag: int) -> int:
    """
    根据用户输入的名称，查询一共有多少个符合要求的文件or文件夹
    :param db:
    :param input_name:
    :param pid:
    :param flag:
        flag=0，是查询文件和文件夹
        flag=1，是查询文件夹
        flag=2，是查询文件
    :return:
    """
    if flag == 0:
        total = db.query(Docs).filter(Docs.name.like('%' + input_name + '%'), Docs.pid == pid).count()
    elif flag == 1 or flag == 2:
        total = db.query(Docs).filter(Docs.name.like('%' + input_name + '%'), Docs.pid == pid,
                                      Docs.flag == flag).count()
    else:
        total = 0
    return total


def get_doc_by_name(db: Session, name: str) -> [Docs]:
    """
    查询新建的文件or文件夹，有没有重名的
    :param db:
    :param name:
    :return:
    """
    docs = db.query(Docs).filter(Docs.name == name).all()
    return docs


def get_pname_by_pid(db: Session, pid: int) -> str:
    """
    给pid，查询pid对应的名称
    :param db:
    :param pid:
    :return:
    """
    doc: Docs = db.query(Docs).filter(Docs.id == pid).first()
    # name_list = ["四级文件夹","三级文件夹","二级文件夹","一级文件夹",]
    name = doc.name
    name_list = [name]
    if doc.pid != 0:
        name_list = get_parent_name(db, doc, name_list)
    return name_list


def get_parent_name(db: Session, doc: Docs, name_list: [str]):
    """
    递归查询parent_name
    :param db:
    :param doc:
    :param name_list:
    :return:
    """
    doc_p: Docs = db.query(Docs).filter(Docs.id == doc.pid).first()
    name_list.append(doc_p.name)
    if doc_p.pid != 0:
        get_parent_name(db, doc_p, name_list)
    return name_list


def add_docs(db: Session, name: str, user_id: int, pid: int, path: str):
    """
    新增文件夹
    :param db:
    :param name:
    :param user_id:
    :param pid:
    :param path:
    :return:
    """
    doc = Docs(
        name=name,
        flag=1,
        pid=pid,
        user_id=user_id,
        filepath=path

    )
    db.add(doc)
    db.commit()
    db.flush()


def get_path_by_pid(db: Session, pid: int) -> str:
    """
    给出parent_id，获取该pid的路径
    :param db:
    :param pid:
    :return:
    """
    doc: Docs = db.query(Docs).filter(Docs.id == pid).first()
    return doc.filepath


def save_upload(db: Session, filename: str, pid: int, flag: int, filepath: str, filetype: str, user_id: int,
                resource_name: str):
    """
    将文件信息存入数据库
    :param db:
    :param filename:
    :param pid:
    :param flag:
    :param filepath:
    :param filetype:
    :param user_id:
    :param resource_name:
    :return:
    """
    doc = Docs(
        name=filename,
        flag=flag,
        pid=pid,
        filepath=filepath,
        filetype=filetype,
        user_id=user_id,
        resouce_name=resource_name
    )

    db.add(doc)
    db.commit()
    db.flush()
