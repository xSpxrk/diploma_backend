from typing import Any, Dict, Optional, Union
from sqlalchemy.orm import Session
from .base import CRUDBase
from backend.app.models.customer import Customer
from backend.app.core.security import hash_password, verify_password

from backend.app.schemas.customer import CustomerCreate, CustomerUpdate


class CRUDCustomer(CRUDBase[Customer, CustomerCreate, CustomerUpdate]):

    def get(self, db: Session, customer_id: int) -> Optional[Customer]:
        return db.query(self.model).filter(self.model.customer_id == customer_id).first()

    def get_by_email(self, db: Session, email: str):
        return db.query(self.model).filter(self.model.email == email).first()

    def create(
            self,
            db: Session,
            obj_in: CustomerCreate
    ) -> Customer:
        new_customer = Customer(
            name=obj_in.name,
            email=obj_in.email,
            phone_number=obj_in.phone_number,
            hashed_password=hash_password(obj_in.password)
        )
        db.add(new_customer)
        db.commit()
        db.refresh(new_customer)
        return new_customer

    def update(
            self,
            db: Session,
            db_obj: Customer,
            obj_in: Union[CustomerUpdate, Dict[str, Any]]
    ) -> Customer:
        if isinstance(obj_in, dict):
            updated_data = obj_in
        else:
            updated_data = obj_in.dict(exclude_unset=True)
        if updated_data["password"]:
            hashed_password = hash_password(updated_data["password"])
            del updated_data["password"]
            updated_data["hashed_password"] = hashed_password
        return super().update(db, db_obj=db_obj, obj_in=updated_data)

    def authenticate(
            self,
            db: Session,
            *,
            email: str,
            password: str
    ) -> Optional[Customer]:
        customer = self.get_by_email(db, email=email)
        if not customer:
            return None
        if not verify_password(password, customer.hashed_password):
            return None
        return customer


customer = CRUDCustomer(Customer)
