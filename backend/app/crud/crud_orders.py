from .base import CRUDBase
from backend.app.models import Order
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from typing import Optional, List
from backend.app.schemas.order import OrderCreate, OrderUpdate
from sqlalchemy import desc, asc


class CRUDOrder(CRUDBase[Order, OrderCreate, OrderUpdate]):
    def get_multi(
            self,
            db: Session,
            skip: int = 0,
            limit: int = 3

    ) -> List[Order]:
        return db.query(self.model).order_by(desc('order_id')).offset(skip).limit(limit).all()

    def get(self, db: Session, order_id: int) -> Optional[Order]:
        return db.query(self.model).filter(self.model.order_id == order_id).first()

    def create(
            self,
            db: Session,
            obj_in: OrderCreate,
            customer_id: int
    ) -> Order:
        new_order = jsonable_encoder(obj_in)
        db_order = self.model(**new_order, customer_id=customer_id)
        db.add(db_order)
        db.commit()
        db.refresh(db_order)
        return db_order


order = CRUDOrder(Order)
