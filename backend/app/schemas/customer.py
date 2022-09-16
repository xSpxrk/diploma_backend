from pydantic import BaseModel, EmailStr
from typing import Optional, List
from .order import Order
from .review import Review


class CustomerBase(BaseModel):
    name: str
    email: EmailStr
    phone_number: Optional[str]


class CustomerCreate(CustomerBase):
    email: EmailStr
    password: str


class Customer(CustomerBase):
    orders: List[Order] = []
    reviews: List[Review] = []

    class Config:
        orm_mode = True


class CustomerUpdate(CustomerBase):
    password: str



