from typing import Any, List
from fastapi.security import OAuth2PasswordBearer
from fastapi import APIRouter, Body, Depends, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session
from backend.app.api import deps
from backend.app import models, schemas
from backend.app import crud

router = APIRouter()


@router.get("/", response_model=List[schemas.Customer], )
def read_customers(
        db: Session = Depends(deps.get_db)
):
    customers = crud.customer.get_multi(db)
    return customers


@router.get('/one', response_model=schemas.Customer)
def read_customer(
        request: Request,
        db: Session = Depends(deps.get_db),
):
    token = request.headers.get('Authorization')
    current_user = deps.get_current_user(db, token=token)

    customer = crud.customer.get_by_email(db, current_user.email)
    customer.reviews = crud.review.get_customer_multi(db, customer.customer_id)
    return customer


@router.get('/{customer_id}', response_model=schemas.Customer)
def read_customer(
        customer_id: int,
        db: Session = Depends(deps.get_db),
):
    customer = crud.customer.get(db, customer_id)
    customer.reviews = crud.review.get_customer_multi(db, customer_id)
    return customer


@router.post('/', response_model=schemas.Customer)
def create_customer(
        *,
        db: Session = Depends(deps.get_db),
        user_in: schemas.CustomerCreate
) -> Any:
    user = crud.customer.get_by_email(db, user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail='The customer exists already'
        )
    user = crud.customer.create(db, user_in)
    return user


@router.put("/{customer_id}", response_model=schemas.Customer)
def update_customer(
        *,
        db: Session = Depends(deps.get_db),
        customer_id: int,
        customer_in: schemas.CustomerUpdate,
) -> Any:
    customer = crud.customer.get(db, customer_id)
    if not customer:
        raise HTTPException(
            status_code=400,
            detail="The customer with this id doesnt exist"
        )
    customer = crud.customer.update(db, db_obj=customer, obj_in=customer_in)
    return customer
