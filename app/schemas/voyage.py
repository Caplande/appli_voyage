# schemas/voyage.py
from pydantic import BaseModel
from datetime import date
from typing import Optional
import app.schemas.voyage as v

print("FICHIER CHARGÉ :", v.__file__)
print("CONTENU :", dir(v))


# 🔹 Base commune
# 🔹 Base commune
class VoyageBase(BaseModel):
    nom: str
    commentaire: Optional[str] = None  # ⚡ ajouté
    date_debut: date
    date_fin: date


# 🔹 Pour la création (POST)
class VoyageCreate(VoyageBase):
    pass


# 🔹 Pour la lecture (GET)
class Voyage(VoyageBase):
    id: int

    class Config:
        from_attributes = True
