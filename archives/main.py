# src/main.py
from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session
from archives import models
from app.database import engine, SessionLocal
from pydantic import BaseModel
from typing import List, Optional
from datetime import date

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# --- Schemas Pydantic ---
class UtilisateurCreate(BaseModel):
    nom: str
    prenom: Optional[str] = None
    date_arrivee: Optional[date] = None
    date_depart: Optional[date] = None


class VoyageCreate(BaseModel):
    nom: str
    commentaire: Optional[str] = None
    date_debut: date
    date_fin: date
    participants: List[UtilisateurCreate]


# --- Route création voyage + participants ---
@app.post("/voyages/")
def creer_voyage(voyage: VoyageCreate):
    db: Session = SessionLocal()
    try:
        nouveau_voyage = models.Voyage(
            nom=voyage.nom,
            commentaire=voyage.commentaire,
            date_debut=voyage.date_debut,
            date_fin=voyage.date_fin,
        )
        db.add(nouveau_voyage)
        db.commit()
        db.refresh(nouveau_voyage)

        for u in voyage.participants:
            utilisateur = models.Utilisateur(
                nom=u.nom,
                prenom=u.prenom,
                date_arrivee=u.date_arrivee,
                date_depart=u.date_depart,
                voyage_id=nouveau_voyage.id,
            )
            db.add(utilisateur)
        db.commit()
        return {"voyage_id": nouveau_voyage.id}
    finally:
        db.close()
