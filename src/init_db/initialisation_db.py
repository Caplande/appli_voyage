from src.database import engine, Base
from src import models  # Importe vos classes Utilisateur, Depense, etc.


def create_tables():
    print("Connexion à PostgreSQL et création des tables...")
    # Cette ligne compare vos modèles Python avec la BDD et crée les tables manquantes
    Base.metadata.create_all(bind=engine)
    print("Tables créées avec succès !")


if __name__ == "__main__":
    create_tables()
