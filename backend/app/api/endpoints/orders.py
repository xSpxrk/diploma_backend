from typing import List
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from backend.app.api import deps
from backend.app import schemas
from backend.app import crud
from backend.app import models

router = APIRouter()


@router.get("/", response_model=List[schemas.Order])
def read_orders(
        skip: int,
        limit: int,
        db: Session = Depends(deps.get_db),

):
    orders = crud.order.get_multi(db, skip, limit)
    headers = {'total': str(len(db.query(models.Order).all()))}
    return orders


@router.get('/max')
def get_max(
        db: Session = Depends(deps.get_db)
):
    return len(db.query(models.Order).all())


@router.get("/{order_id}", response_model=schemas.Order)
def read_order(
        *,
        db: Session = Depends(deps.get_db),
        order_id: int,
):
    order = crud.order.get(db, order_id)
    return order


@router.post("/", response_model=schemas.Order)
def create_order(
        *,
        db: Session = Depends(deps.get_db),
        order_in: schemas.OrderCreate,
        token: str
):
    customer = deps.get_current_user(db, token)
    customer_id = customer.customer_id
    order = crud.order.create(db, order_in, customer_id)
    return order


@router.put("/update/{order_id}", response_model=schemas.Order)
def update_order(
        *,
        db: Session = Depends(deps.get_db),
        order_in: schemas.OrderUpdate,
        order_id: int
):
    order = crud.order.get(db, order_id)
    if not order:
        raise HTTPException(
            status_code=404,
            detail="The offer with this id doesnt exist"
        )
    order = crud.order.update(db, db_obj=order, obj_in=order_in)
    return order


@router.delete('/{order_id}', response_model=schemas.Order)
def delete_order(
        *,
        db: Session = Depends(deps.get_db),
        order_id: int
):
    order = crud.order.remove(db, order_id)
    return order
