from typing import Any, List, Union, Optional, Tuple
from fastapi.security import OAuth2PasswordBearer
from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from backend.app.core.security import hash_password
from sqlalchemy.orm import Session
from backend.app.api import deps
from backend.app import models, schemas
from backend.app import crud

router = APIRouter()


@router.get('/', response_model=Union[schemas.Provider, schemas.Customer])
def read_me(
        *,
        db: Session = Depends(deps.get_db),
        token: str
):
    current_user = deps.get_current_user(db, token)
    if isinstance(current_user, models.Customer):
        user = crud.customer.get(db, current_user.customer_id)
        user.reviews = crud.review.get_customer_multi(db, user.customer_id)
    else:
        user = crud.provider.get(db, current_user.provider_id)
        user.reviews = crud.review.get_provider_multi(db, user.provider_id)
    return user


@router.put("/", response_model=Union[schemas.Customer, schemas.Provider])
def update_me(
        *,
        db: Session = Depends(deps.get_db),
        user_in: Union[schemas.ProviderUpdate, schemas.CustomerUpdate],
        token: str
) -> Any:
    current_user = deps.get_current_user(db, token)
    if isinstance(current_user, models.Customer):
        obj = crud.customer.get(db, current_user.customer_id)
        user = crud.customer.update(db, db_obj=obj, obj_in=user_in)
    else:
        obj = crud.provider.get(db, current_user.provider_id)
        user = crud.provider.update(db, db_obj=obj, obj_in=user_in)
    return user
