from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.membre import Membre
from app.schemas.membre import MembreCreate, Membre as MembreSchema
from app.models.participation import ParticipationVoyage
from app.models.voyage import Voyage

router = APIRouter()


@router.post("/", response_model=MembreSchema)
def create_membre(membre: MembreCreate, db: Session = Depends(get_db)):
    db_membre = Membre(**membre.dict())
    db.add(db_membre)
    db.commit()
    db.refresh(db_membre)
    return db_membre


@router.get("/", response_model=list[MembreSchema])
def list_membres(db: Session = Depends(get_db)):
    return db.query(Membre).all()


@router.post("/{voyage_id}/membres", response_model=MembreSchema)
def add_membre_to_voyage(
    voyage_id: int, membre: MembreCreate, db: Session = Depends(get_db)
):
    # création du membre
    db_membre = Membre(**membre.dict())
    db.add(db_membre)
    db.commit()
    db.refresh(db_membre)

    # récupérer le voyage
    voyage = db.query(Voyage).get(voyage_id)

    # créer la participation par défaut avec dates du voyage
    participation = ParticipationVoyage(
        voyage_id=voyage.id,
        membre_id=db_membre.id,
        date_arrivee=voyage.date_debut,
        date_depart=voyage.date_fin,
    )
    db.add(participation)
    db.commit()
    return db_membre
