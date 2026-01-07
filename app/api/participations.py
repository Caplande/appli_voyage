from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.participation import ParticipationCreate, Participation
from app.models.participation import ParticipationVoyage as ParticipationModel
from app.database import get_db

router = APIRouter()


@router.post("/voyages/{voyage_id}/participations", response_model=Participation)
def add_participation(
    voyage_id: int, p: ParticipationCreate, db: Session = Depends(get_db)
):
    # dates par défaut si non fournies
    from models.voyage import Voyage

    voyage = db.query(Voyage).get(voyage_id)
    date_arrivee = p.date_arrivee or voyage.date_debut
    date_depart = p.date_depart or voyage.date_fin

    participation = ParticipationModel(
        voyage_id=voyage_id,
        membre_id=p.membre_id,
        date_arrivee=date_arrivee,
        date_depart=date_depart,
    )
    db.add(participation)
    db.commit()
    db.refresh(participation)
    return participation
