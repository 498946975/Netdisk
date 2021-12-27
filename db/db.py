from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

username = "root"
pwd = "123"
host = "81.70.88.52"
port = "3306"
db_name = "test_fastapi"

url = "mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8".format(username, pwd, host, port, db_name)

Engine = create_engine(url)

LocalSession = sessionmaker(bind=Engine)

Base = declarative_base()
