from pydantic import BaseModel
from datetime import date


class ParticipationCreate(BaseModel):
    membre_id: int
    date_arrivee: date | None = None
    date_depart: date | None = None


class Participation(ParticipationCreate):
    id: int

    class Config:
        orm_mode = True
