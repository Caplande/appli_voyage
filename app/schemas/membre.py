from pydantic import BaseModel, EmailStr
from typing import Optional


class MembreCreate(BaseModel):
    nom: str
    prenom: str
    email: Optional[EmailStr] = None
    mobile: Optional[str] = None


class Membre(MembreCreate):
    id: int

    class Config:
        orm_mode = True
