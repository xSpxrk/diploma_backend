from .base import CRUDBase
from backend.app.models import Material
from sqlalchemy.orm import Session
from typing import Optional, List
from backend.app.schemas.offer import OfferCreate, OfferUpdate


class CRUDMaterial(CRUDBase[Material, OfferCreate, OfferUpdate]):
    def get_multi(
            self,
            db: Session,
    ) -> List[Material]:
        return db.query(self.model).filter().all()


material = CRUDMaterial(Material)
