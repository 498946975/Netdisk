from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from apps.config.settings import settings



url = settings.DB_TEST_URL

Engine = create_engine(url)

LocalSession = sessionmaker(bind=Engine)

Base = declarative_base()
