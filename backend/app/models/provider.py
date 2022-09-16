from sqlalchemy import Integer, Column, String, BigInteger
from sqlalchemy.orm import relationship
from backend.app.db.base_class import Base


class Provider(Base):
    provider_id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    phone_number = Column(String)
    hashed_password = Column(String)
    offers = relationship("Offer", back_populates="provider")
    reviews = relationship('Review', back_populates='provider')

    def __repr__(self):
        return self.name
