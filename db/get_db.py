from .db import LocalSession


def get_db():
    try:
        db = LocalSession()
        yield db
    finally:
        db.close()
