from pydantic import BaseModel
from .offer import Offer
from typing import List
from .material import Material
from pydantic.schema import Optional


class OrderBase(BaseModel):
    name: str
    description: str
    material_id: int
    quantity: int


class Order(OrderBase):
    order_id: int
    offers: List[Offer]
    customer_id: int
    material: Optional[Material]

    class Config:
        orm_mode = True


class OrderCreate(OrderBase):
    pass


class OrderUpdate(OrderBase):
    pass
