from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Example: postgresql://user:password@postgresserver/dbname
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/mydatabase"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()