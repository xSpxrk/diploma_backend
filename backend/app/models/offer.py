from sqlalchemy import Integer, Column, String, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from backend.app.db.base_class import Base


class Offer(Base):
    offer_id = Column(Integer, primary_key=True)
    quantity = Column(Integer)
    price = Column(DECIMAL)
    order_id = Column(Integer, ForeignKey("orders.order_id"))
    order = relationship("Order", back_populates="offers")
    provider_id = Column(Integer, ForeignKey("providers.provider_id"))
    provider = relationship("Provider", back_populates="offers")
