# src/models.py
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text, Float
from sqlalchemy.orm import relationship
from app.database import Base


class Voyage(Base):
    __tablename__ = "voyages"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, nullable=False)
    date_debut = Column(Date, nullable=False)
    date_fin = Column(Date, nullable=False)

    participations = relationship(
        "ParticipationVoyage", back_populates="voyage", cascade="all, delete-orphan"
    )


class Membre(Base):
    __tablename__ = "membres"

    id = Column(Integer, primary_key=True, index=True)

    nom = Column(String, nullable=False)
    prenom = Column(String, nullable=False)

    email = Column(String, nullable=True, index=True)
    mobile = Column(String, nullable=True)

    participations = relationship("ParticipationVoyage", back_populates="membre")


class Depense(Base):
    __tablename__ = "depenses"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    montant = Column(Float, nullable=False)

    payeur_id = Column(Integer, ForeignKey("membres.id"), nullable=False)

    voyage_id = Column(Integer, ForeignKey("voyages.id"), nullable=False)
    voyage = relationship("Voyage", back_populates="depenses")
