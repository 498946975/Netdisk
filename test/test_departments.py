from utils.user_operation import get_departments
from db.get_db import get_db

if __name__ == '__main__':
    db = get_db()
    a = get_departments(db)
    print(a)