from pydantic import BaseModel
from typing import List, Optional


class ReviewBase(BaseModel):
    description: str = ''
    rating: int = 0


class Review(ReviewBase):
    review_id: int
    provider_id: int
    customer_id: int
    owner: int
    isShow: bool | None

    class Config:
        orm_mode = True


class ReviewCreate(ReviewBase):
    pass


class ReviewUpdate(ReviewBase):
    pass
