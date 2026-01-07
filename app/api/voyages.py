from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.voyage import VoyageCreate, Voyage
from app.models.voyage import Voyage as VoyageModel
from app.database import get_db

router = APIRouter()


@router.post("/voyages", response_model=Voyage)
def create_voyage(voyage: VoyageCreate, db: Session = Depends(get_db)):
    db_voyage = VoyageModel(**voyage.dict())
    db.add(db_voyage)
    db.commit()
    db.refresh(db_voyage)
    return db_voyage
