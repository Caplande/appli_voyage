from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import pandas as pd
from app.database import get_db
from app.models.voyage import Voyage
from app.models.membre import Membre

router = APIRouter(prefix="/voyages", tags=["Export"])


@router.get("/{voyage_id}/soldes")
def get_soldes(voyage_id: int, db: Session = Depends(get_db)):
    voyage = db.query(Voyage).get(voyage_id)
    membres_soldes = {p.membre_id: 0.0 for p in voyage.participations}
    for dep in voyage.depenses:
        nb = len(voyage.participations)
        partage = dep.montant / nb
        for p in voyage.participations:
            membres_soldes[p.membre_id] -= partage
        membres_soldes[dep.payeur_id] += dep.montant
    return {
        db.query(Membre).get(mid).prenom: solde for mid, solde in membres_soldes.items()
    }


@router.get("/{voyage_id}/export")
def export_excel(voyage_id: int, db: Session = Depends(get_db)):
    voyage = db.query(Voyage).get(voyage_id)
    participants = [
        {
            "Nom": p.membre.nom,
            "Prénom": p.membre.prenom,
            "Email": p.membre.email,
            "Mobile": p.membre.mobile,
            "Date arrivée": p.date_arrivee,
            "Date départ": p.date_depart,
        }
        for p in voyage.participations
    ]
    df_part = pd.DataFrame(participants)

    depenses = [
        {
            "Description": d.description,
            "Date": d.date,
            "Montant": d.montant,
            "Payeur": d.payeur.prenom + " " + d.payeur.nom,
        }
        for d in voyage.depenses
    ]
    df_dep = pd.DataFrame(depenses)

    soldes = {p.membre_id: 0.0 for p in voyage.participations}
    for d in voyage.depenses:
        nb = len(voyage.participations)
        partage = d.montant / nb
        for p in voyage.participations:
            soldes[p.membre_id] -= partage
        soldes[d.payeur_id] += d.montant
    df_soldes = pd.DataFrame(
        [
            {
                "Nom": db.query(Membre).get(mid).nom,
                "Prénom": db.query(Membre).get(mid).prenom,
                "Solde": solde,
            }
            for mid, solde in soldes.items()
        ]
    )

    filename = f"voyage_{voyage_id}.xlsx"
    with pd.ExcelWriter(filename) as writer:
        df_part.to_excel(writer, sheet_name="Participants", index=False)
        df_dep.to_excel(writer, sheet_name="Dépenses", index=False)
        df_soldes.to_excel(writer, sheet_name="Soldes", index=False)
    return FileResponse(
        filename,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename=filename,
    )
