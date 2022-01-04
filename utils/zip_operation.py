import os
import zipfile
from models.docs.docs_model import Docs
from sqlalchemy.orm import Session


def zip_dir(output_file, dir):
    """
    单个文件夹打包下载
    :param output_file:
    :param dir:
    :return:
    """
    zp = zipfile.ZipFile(output_file, "w")
    for path, dirname, filenames in os.walk(dir):
        # 去掉uploads/docs/这个层级
        fpath = path.replace(dir, "")
        for filename in filenames:
            zp.write(os.path.join(path, filename), os.path.join(fpath, filename))
    zp.close()


def zip_file_or_dir(db: Session, output_file, docs: [Docs]):
    """
    打包多个文件+文件夹
    :param db:
    :param output_file:
    :param docs:
    :return:
    """
    zp = zipfile.ZipFile(output_file, "w")
    for doc in docs:
        if doc.flag == 1:  # 文件夹
            for path, dirname, filenames in os.walk(doc.filepath):
                fpath = path.replace(doc.filepath.rsplit("/", 1)[0], "")
                for filename in filenames:
                    zp.write(os.path.join(path, filename), os.path.join(fpath, filename))
        else:   # 文件
            p_doc = db.query(Docs).filter(Docs.id == doc.pid).first()
            fpath = doc.filepath.replace(p_doc.filepath, "")
            zp.write(doc.filepath, os.path.join(fpath, doc.name))
    zp.close()
