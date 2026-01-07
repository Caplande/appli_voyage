# src/routers/voyages.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date

from app.database import SessionLocal
from archives import models

router = APIRouter(prefix="/voyages", tags=["Voyages"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def creer_voyage(payload: dict, db: Session = Depends(get_db)):
    voyage = models.Voyage(
        nom=payload["nom"],
        commentaire=payload.get("commentaire"),
        date_debut=date.fromisoformat(payload["date_debut"]),
        date_fin=date.fromisoformat(payload["date_fin"]),
    )
    db.add(voyage)
    db.flush()

    for u in payload["utilisateurs"]:
        utilisateur = models.Utilisateur(
            nom=u["nom"],
            prenom=u["prenom"],
            date_arrivee=date.fromisoformat(u["date_arrivee"]),
            date_depart=date.fromisoformat(u["date_depart"]),
            voyage_id=voyage.id,
        )
        db.add(utilisateur)

    db.commit()

    return {"voyage_id": voyage.id}
