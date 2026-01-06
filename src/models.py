from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from src.database import Base


class Utilisateur(Base):
    __tablename__ = "utilisateurs"
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, unique=True, nullable=False)

    # ✅ Relation vers les dépenses qu'il a payées
    depenses_payees = relationship("Depense", back_populates="payeur")

    # ✅ Relation vers les répartitions dont il est bénéficiaire
    repartitions = relationship("Repartition", back_populates="beneficiaire")


class Depense(Base):
    __tablename__ = "depenses"
    id = Column(Integer, primary_key=True)
    description = Column(String, nullable=False)
    montant = Column(Float, nullable=False)
    payeur_id = Column(Integer, ForeignKey("utilisateurs.id"), nullable=False)

    # ✅ Lien vers le payeur
    payeur = relationship("Utilisateur", back_populates="depenses_payees")

    # ✅ Lien vers les répartitions de cette dépense
    repartitions = relationship(
        "Repartition", back_populates="depense", cascade="all, delete-orphan"
    )


class Repartition(Base):
    __tablename__ = "repartitions"
    id = Column(Integer, primary_key=True)
    depense_id = Column(Integer, ForeignKey("depenses.id"), nullable=False)
    beneficiaire_id = Column(Integer, ForeignKey("utilisateurs.id"), nullable=False)
    part = Column(Float, nullable=False)

    # ✅ Lien vers la dépense
    depense = relationship("Depense", back_populates="repartitions")

    # ✅ Lien vers le bénéficiaire
    beneficiaire = relationship("Utilisateur", back_populates="repartitions")
