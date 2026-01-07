from datetime import date
from sqlalchemy.orm import Session
from app.database import SessionLocal, Base, engine
from app.models.voyage import Voyage
from app.models.membre import Membre
from app.models.participation import ParticipationVoyage
from app.models.depense import Depense

# 1️⃣ Créer les tables (au cas où)
Base.metadata.create_all(bind=engine)

# 2️⃣ Ouvrir une session
db: Session = SessionLocal()

try:
    # --- RAZ complète des tables ---
    # ordre important pour respecter les ForeignKey
    db.query(Depense).delete()
    db.query(ParticipationVoyage).delete()
    db.query(Voyage).delete()
    db.query(Membre).delete()
    db.commit()
    print("Toutes les tables ont été réinitialisées")
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
        date_arrivee=date(2026, 5, 12),
        date_depart=date(2026, 5, 18),
    )
    db.add_all([p1, p2])
    db.commit()
    print("Participations ajoutées")

    # --- ajouter 2 dépenses ---
    dep1 = Depense(
        description="Hôtel",
        date=date(2026, 5, 11),
        montant=200,
        payeur_id=alice.id,
        voyage_id=voyage.id,
    )
    dep2 = Depense(
        description="Dîner",
        date=date(2026, 5, 12),
        montant=120,
        payeur_id=bob.id,
        voyage_id=voyage.id,
    )
    db.add_all([dep1, dep2])
    db.commit()
    print("Dépenses ajoutées")

    # --- fonction pour calculer les soldes ---
    def calculer_soldes(voyage_id: int, db: Session):
        voyage = db.query(Voyage).get(voyage_id)
        membres = {p.membre_id: 0.0 for p in voyage.participations}

        for dep in voyage.depenses:
            nb_participants = len(voyage.participations)
            partage = dep.montant / nb_participants
            for p in voyage.participations:
                membres[p.membre_id] -= partage
            membres[dep.payeur_id] += dep.montant
        return membres

    # --- calculer et afficher les soldes ---
    soldes = calculer_soldes(voyage.id, db)
    print("Soldes finaux :")
    for membre_id, solde in soldes.items():
        membre = db.query(Membre).get(membre_id)
        print(f"{membre.prenom} {membre.nom}: {solde:.2f} €")

finally:
    db.close()
