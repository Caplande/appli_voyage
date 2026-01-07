# src/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

print("database importée avec succès")

DATABASE_URL = "postgresql+psycopg2://postgres:PO1357po@localhost:5432/voyages"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# la fonction get_db
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
