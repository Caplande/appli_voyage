from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.voyage import Voyage as VoyageModel
from app.schemas.voyage import VoyageCreate, Voyage as VoyageSchema

router = APIRouter(prefix="/voyages", tags=["Voyages"])


@router.post("/", response_model=VoyageSchema)
def creer_voyage(voyage: VoyageCreate, db: Session = Depends(get_db)):
    db_voyage = VoyageModel(
        nom=voyage.nom,
        commentaire=voyage.commentaire,
        date_debut=voyage.date_debut,
        date_fin=voyage.date_fin,
    )
    db.add(db_voyage)
    db.commit()
    db.refresh(db_voyage)
    print("PAYLOAD RECU :", voyage)
    return db_voyage


# --- Lister tous les voyages ---
@router.get("/", response_model=list[VoyageSchema])
def list_voyages(db: Session = Depends(get_db)):
    return db.query(VoyageModel).all()


# --- Nouvel endpoint : lister voyages + voyage par défaut ---


@router.get("/derniers_voyages")
def derniers_voyages(db: Session = Depends(get_db)):
    voyages = db.query(VoyageModel).order_by(VoyageModel.id.desc()).all()
    voyage_defaut = voyages[0] if voyages else None

    voyages_json = [
        {
            "id": v.id,
            "nom": v.nom,
            "date_debut": v.date_debut.isoformat(),
            "date_fin": v.date_fin.isoformat(),
        }
        for v in voyages
    ]

    return {
        "voyages": voyages_json,
        "voyage_defaut_id": voyage_defaut.id if voyage_defaut else None,
    }
