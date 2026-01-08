import uvicorn
from app.database import Base, engine
from app.main import app

# --- 1️⃣ Drop toutes les tables (RAZ totale) ---
print("Suppression de toutes les tables existantes…")
Base.metadata.drop_all(bind=engine)
print("Tables supprimées.")

# --- 2️⃣ Création de toutes les tables ---
print("Création des tables…")
Base.metadata.create_all(bind=engine)
print("Tables créées.")

# --- 3️⃣ Lancer le serveur FastAPI ---
if __name__ == "__main__":
    print("Démarrage du serveur FastAPI sur http://localhost:8000 …")
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
