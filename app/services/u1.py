from sqlalchemy.orm import Session
from app.models.voyage import Voyage
from app.database import Base, engine


def creer_tables():
    # créer les tables si elles n'existent pas
    Base.metadata.create_all(bind=engine)


def calculer_soldes(voyage_id: int, db: Session):
    voyage = db.query(Voyage).get(voyage_id)
    membres = {p.membre_id: 0.0 for p in voyage.participations}

    for dep in voyage.depenses:
        nb_participants = len(voyage.participations)
        partage = dep.montant / nb_participants
        for p in voyage.participations:
            membres[p.membre_id] -= partage
        membres[dep.payeur_id] += dep.montant

    # retourne dict {membre_id: solde}
    return membres


if __name__ == "__main__":
    creer_tables()
    print("Tables créées avec succès.")
