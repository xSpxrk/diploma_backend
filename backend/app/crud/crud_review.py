from .base import CRUDBase
from backend.app.models import Review
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from typing import Optional, List
from backend.app.schemas.review import ReviewCreate, ReviewUpdate


class CRUDReview(CRUDBase[Review, ReviewCreate, ReviewUpdate]):
    def create(
            self,
            db: Session,
            obj_in: ReviewCreate,
            owner: int,
            customer_id: int,
            provider_id: int

    ) -> Review:
        new_review = Review(
            owner=owner,
            description=obj_in.description,
            customer_id=customer_id,
            provider_id=provider_id,
            rating=obj_in.rating
        )
        db.add(new_review)
        db.commit()
        db.refresh(new_review)
        return new_review

    def get_provider_multi(
            self,
            db: Session,
            provider_id: int

    ):
        return db.query(self.model).filter(
            self.model.provider_id == provider_id,
            self.model.owner == 0,
            self.model.isShow == 'true'
        ).all()

    def get_customer_multi(
            self,
            db: Session,
            customer_id: int

    ):
        return db.query(self.model).filter(
            self.model.customer_id == customer_id,
            self.model.owner == 1,
            self.model.isShow == 'true'
        ).all()


review = CRUDReview(Review)
