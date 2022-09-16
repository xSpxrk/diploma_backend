from sqlalchemy import Integer, Column, String, ForeignKey, DECIMAL, Boolean
from sqlalchemy.orm import relationship
from backend.app.db.base_class import Base


class Review(Base):
    review_id = Column(Integer, primary_key=True)
    description = Column(String)
    rating = Column(Integer)
    customer_id = Column(Integer, ForeignKey('customers.customer_id'))
    provider_id = Column(Integer, ForeignKey('providers.provider_id'))
    owner = Column(Integer)
    isShow = Column(Boolean)
    provider = relationship('Provider', back_populates='reviews')
    customer = relationship('Customer', back_populates='reviews')
