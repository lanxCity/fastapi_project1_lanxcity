from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import settings

# for the database url, we have:
# postgresql://<username>:<password>@<ip addr/hostname>/<db_name>


# SQLALCHEMY_DB_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

SQLALCHEMY_DB_URL =settings.database_url

# Create the connection engine
engine = create_engine(SQLALCHEMY_DB_URL)

# Create a session factory to be able query the db
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a Base class for your ORM models to inherit
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()