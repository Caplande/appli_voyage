from pydantic import BaseModel
from typing import List


# Ce qui est nécessaire pour créer un utilisateur
class UtilisateurCreate(BaseModel):
    nom: str


# Ce qui est envoyé quand on crée une dépense
class DepenseCreate(BaseModel):
    description: str
    montant: float
    payeur_id: int
    beneficiaire_ids: List[int]


# (Optionnel) Ce que l'API renvoie (pour inclure l'ID généré)
class Utilisateur(BaseModel):
    id: int
    nom: str

    class Config:
        from_attributes = True
