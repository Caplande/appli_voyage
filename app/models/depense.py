from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Depense(Base):
    __tablename__ = "depenses"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    montant = Column(Float, nullable=False)

    payeur_id = Column(Integer, ForeignKey("membres.id"), nullable=False)
    voyage_id = Column(Integer, ForeignKey("voyages.id"), nullable=False)

    payeur = relationship("Membre")
    voyage = relationship("Voyage", back_populates="depenses")
