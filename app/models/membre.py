from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

print("models/membre importé avec succès")


class Membre(Base):
    __tablename__ = "membres"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, nullable=False)
    prenom = Column(String, nullable=False)
    email = Column(String, nullable=True)
    mobile = Column(String, nullable=True)

    participations = relationship("ParticipationVoyage", back_populates="membre")
