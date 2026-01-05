from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Remplacez par vos identifiants PostgreSQL
SQLALCHEMY_DATABASE_URL = (
    "postgresql+psycopg2://postgres:PO1357po@127.0.0.1:5432/voyages"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
