from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import session, sessionmaker
from ..config import config

USERNAME = config.settings.DB_USERNAME
PASSWORD = config.settings.DB_PASSWORD
HOSTNAME = config.settings.DB_HOSTNAME
PORT = config.settings.DB_PORT
DATABASE_NAME = config.settings.DB_NAME

SQLALCHEMY_DATBASE_URL = f'postgresql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE_NAME}'
engine = create_engine(SQLALCHEMY_DATBASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

#Dependency
def get_db():
    db = SessionLocal()
    try:
        print("Connected to DB succeeded!")
        yield db
    except Exception as error:
        print("Connection to DB failed!")
        print("Error: ", error)
        
    finally:
        print("Connection to DB closed!")
        db.close()
           
        
