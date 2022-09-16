from pydantic import BaseModel
from decimal import Decimal
from typing import List, Optional


class OfferBase(BaseModel):
    quantity: int
    price: Decimal
    order_id: int
    provider_id: Optional[int] = None


class Offer(OfferBase):
    offer_id: int

    class Config:
        orm_mode = True


class OfferCreate(OfferBase):
    pass


class OfferUpdate(OfferBase):
    pass
