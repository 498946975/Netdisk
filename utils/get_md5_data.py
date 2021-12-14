import hashlib


def get_md5_pwd(pwd: str):
    m = hashlib.md5()
    m.update(pwd.encode('utf-8'))
    return m.hexdigest()
