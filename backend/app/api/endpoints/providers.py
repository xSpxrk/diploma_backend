from typing import List, Any
from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from backend.app.api import deps
from backend.app import schemas
from backend.app import crud

router = APIRouter()


@router.get("/", response_model=List[schemas.Provider])
def read_providers(
        db: Session = Depends(deps.get_db)
):
    providers = crud.provider.get_multi(db)
    return providers


@router.get('/one', response_model=schemas.Provider)
def read_customer(
        request: Request,
        db: Session = Depends(deps.get_db),
):
    token = request.headers.get('Authorization')
    current_user = deps.get_current_user(db, token=token)
    provider = crud.provider.get_by_email(db, current_user.email)
    provider.reviews = crud.review.get_provider_multi(db, provider.provider_id)
    return provider


@router.get("/{provider_id}", response_model=schemas.Provider)
def read_provider(
        provider_id: int,
        db: Session = Depends(deps.get_db)
):
    provider = crud.provider.get(db, provider_id)
    provider.reviews = crud.review.get_provider_multi(db, provider_id)
    return provider


@router.post('/', response_model=schemas.Provider)
def create_customer(
        *,
        db: Session = Depends(deps.get_db),
        user_in: schemas.ProviderCreate
) -> Any:
    user = crud.provider.get_by_email(db, user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail='The provider exists already'
        )
    user = crud.provider.create(db, user_in)
    return user
