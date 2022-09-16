from sqlalchemy import Integer, Column, String, ForeignKey, DECIMAL, Boolean
from sqlalchemy.orm import relationship
from backend.app.db.base_class import Base


class Material(Base):
    material_id = Column(Integer, primary_key=True)
    name = Column(String)
    order = relationship("Order", back_populates='material')

