from datetime import date
from sqlalchemy.orm import Session
from app.database import SessionLocal, Base, engine
from app.models.voyage import Voyage
from app.models.membre import Membre
from app.models.participation import ParticipationVoyage

# 1️⃣ créer toutes les tables (au cas où)
Base.metadata.create_all(bind=engine)

# 2️⃣ ouvrir une session
db: Session = SessionLocal()

try:
    # --- créer un voyage ---
    voyage = Voyage(
        nom="Séjour à Rome", date_debut=date(2026, 5, 10), date_fin=date(2026, 5, 20)
    )
    db.add(voyage)
    db.commit()
    db.refresh(voyage)
    print(f"Voyage créé: {voyage.nom} (id={voyage.id})")

    # --- créer 2 membres ---
    alice = Membre(
        nom="Dupont", prenom="Alice", email="alice@mail.com", mobile="0612345678"
    )
    bob = Membre(nom="Martin", prenom="Bob", email="bob@mail.com", mobile="0698765432")
    db.add_all([alice, bob])
    db.commit()
    db.refresh(alice)
    db.refresh(bob)
    print(f"Membres créés: {alice.prenom} (id={alice.id}), {bob.prenom} (id={bob.id})")

    # --- ajouter les participations ---
    p1 = ParticipationVoyage(
        voyage_id=voyage.id,
        membre_id=alice.id,
        date_arrivee=voyage.date_debut,
        date_depart=voyage.date_fin,
    )
    p2 = ParticipationVoyage(
        voyage_id=voyage.id,
        membre_id=bob.id,
        date_arrivee=date(2026, 5, 12),  # Bob arrive plus tard
        date_depart=date(2026, 5, 18),  # Bob repart avant la fin
    )
    db.add_all([p1, p2])
    db.commit()
    db.refresh(p1)
    db.refresh(p2)
    print(
        f"Participations ajoutées: Alice ({p1.date_arrivee}→{p1.date_depart}), Bob ({p2.date_arrivee}→{p2.date_depart})"
    )

finally:
    db.close()
