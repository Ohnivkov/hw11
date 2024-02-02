from fastapi import HTTPException

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.conf.config import config
from starlette import status

url = config.DB_URL
Base = declarative_base()
engine = create_engine(url, echo=False, pool_size=5)
DBSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)


# Dependency
def get_db():
    db = DBSession()
    try:
        yield db
    except SQLAlchemyError as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))
    finally:
        db.close()
