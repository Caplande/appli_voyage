from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from app.database import Base

print("models/voyage importé avec succès")


class Voyage(Base):
    __tablename__ = "voyages"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, nullable=False)
    commentaire = Column(String, nullable=True)
    date_debut = Column(Date, nullable=False)
    date_fin = Column(Date, nullable=False)

    participations = relationship(
        "ParticipationVoyage", back_populates="voyage", cascade="all, delete-orphan"
    )
    depenses = relationship(
        "Depense", back_populates="voyage", cascade="all, delete-orphan"
    )
