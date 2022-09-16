from sqlalchemy.orm import Session
from .base import CRUDBase
from backend.app.models import Provider
from backend.app.schemas.provider import ProviderCreate, ProviderUpdate
from typing import Union, Any, Dict, Optional
from backend.app.core.security import hash_password, verify_password


class CRUDProvider(CRUDBase[Provider, ProviderCreate, ProviderUpdate]):

    def get(self, db: Session, provider_id: int) -> Provider:
        return db.query(self.model).filter(self.model.provider_id == provider_id).first()

    def get_by_email(self, db: Session, email: str):
        return db.query(self.model).filter(self.model.email == email).first()

    def create(
            self,
            db: Session,
            obj_in: ProviderCreate
    ) -> Provider:
        new_provider = Provider(
            name=obj_in.name,
            email=obj_in.email,
            phone_number=obj_in.phone_number,
            hashed_password=hash_password(obj_in.password)
        )
        db.add(new_provider)
        db.commit()
        db.refresh(new_provider)
        return new_provider

    def update(
            self,
            db: Session,
            db_obj: Provider,
            obj_in: Union[ProviderUpdate, Dict[str, Any]]
    ) -> Provider:
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
    ) -> Optional[Provider]:
        provider = self.get_by_email(db, email=email)
        if not provider:
            return None
        if not verify_password(password, provider.hashed_password):
            return None
        return provider


provider = CRUDProvider(Provider)
