from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.depense import DepenseCreate, Depense
from app.models.depense import Depense as DepenseModel
from app.database import get_db

router = APIRouter()


@router.post("/depenses/", response_model=Depense)
def create_depense(depense: DepenseCreate, db: Session = Depends(get_db)):
    db_depense = DepenseModel(**depense.dict())
    db.add(db_depense)
    db.commit()
    db.refresh(db_depense)
    return db_depense
