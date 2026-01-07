from sqlalchemy import Column, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.database import Base

print("models/participation importé avec succès")


class ParticipationVoyage(Base):
    __tablename__ = "participations_voyage"

    id = Column(Integer, primary_key=True, index=True)
    voyage_id = Column(Integer, ForeignKey("voyages.id"), nullable=False)
    membre_id = Column(Integer, ForeignKey("membres.id"), nullable=False)
    date_arrivee = Column(Date, nullable=False)
    date_depart = Column(Date, nullable=False)

    voyage = relationship("Voyage", back_populates="participations")
    membre = relationship("Membre", back_populates="participations")
