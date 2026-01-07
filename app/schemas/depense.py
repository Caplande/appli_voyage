from pydantic import BaseModel
from datetime import date


class DepenseCreate(BaseModel):
    description: str
    date: date
    montant: float
    payeur_id: int
    voyage_id: int


class Depense(DepenseCreate):
    id: int

    class Config:
        orm_mode = True
