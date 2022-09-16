from typing import Generator, Union
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from fastapi import Depends
from backend.app import models
from fastapi import HTTPException, status
from jose import jwt
import secrets
from backend.app.core import security
from backend.app.db.session import SessionLocal
from backend.app import schemas, crud
from pydantic import ValidationError

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl="token",

)


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_current_user(
        db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> Union[models.Customer, models.Provider]:
    try:
        payload = jwt.get_unverified_claims(token)
        token_data = schemas.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials"
        )
    if token_data.type == "customer":
        user = crud.customer.get(db, customer_id=token_data.sub)
    else:
        user = crud.provider.get(db, provider_id=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
