from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from src.database import Base


class Utilisateur(Base):
    __tablename__ = "utilisateurs"
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, unique=True)


class Depense(Base):
    __tablename__ = "depenses"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    montant = Column(Float)
    payeur_id = Column(Integer, ForeignKey("utilisateurs.id"))

    payeur = relationship("Utilisateur")
    repartitions = relationship("Repartition", back_populates="depense")


class Repartition(Base):
    __tablename__ = "repartitions"
    id = Column(Integer, primary_key=True, index=True)
    depense_id = Column(Integer, ForeignKey("depenses.id"))
    beneficiaire_id = Column(Integer, ForeignKey("utilisateurs.id"))
    part = Column(Float)

    depense = relationship("Depense", back_populates="repartitions")
    beneficiaire = relationship("Utilisateur")
