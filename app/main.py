from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# importer tous les modèles avant de créer les tables
from app.models import membre, voyage, participation
from app.api import voyages, participations, depenses, export, membres
from app.database import Base, engine


# créer les tables si elles n'existent pas
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(voyages.router)
app.include_router(participations.router)
app.include_router(depenses.router)
app.include_router(membres.router)
app.include_router(export.router)

# Frontend
app.mount("/static", StaticFiles(directory="frontend"), name="static")
