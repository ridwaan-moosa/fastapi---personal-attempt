from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@ip adress or hostname/db name"
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:0165562314@localhost/Fastapi"
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db(): ##copy paste opens and closes db connection
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()
        
## just have to copy nad paste dont need to understand or memorise 