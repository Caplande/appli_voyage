from pydantic import BaseModel
from datetime import date


class VoyageCreate(BaseModel):
    nom: str
    date_debut: date
    date_fin: date


class Voyage(VoyageCreate):
    id: int

    class Config:
        orm_mode = True
