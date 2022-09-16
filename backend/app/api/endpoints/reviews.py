from typing import List
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from backend.app.api import deps
from backend.app import schemas
from backend.app import crud
from backend.app import models

router = APIRouter()


@router.get('/')
def read_reviews(
        db: Session = Depends(deps.get_db)
):
    reviews = crud.review.get_multi(db)
    return reviews


@router.post('/')
def create_review(
        *,
        db: Session = Depends(deps.get_db),
        review_in: schemas.ReviewCreate,
        user_id: int,
        token: str
):
    current_user = deps.get_current_user(db, token)
    if isinstance(current_user, models.Customer):
        owner = 0
        review = crud.review.create(db, review_in, owner, current_user.customer_id, user_id)
    else:
        owner = 1
        review = crud.review.create(db, review_in, owner, user_id, current_user.provider_id)
    return review


@router.get('/rating')
def get_rating(
        *,
        db: Session = Depends(deps.get_db),
        token: str
):
    current_user = deps.get_current_user(db, token)
    if isinstance(current_user, models.Customer):
        reviews = crud.review.get_customer_multi(db, current_user.customer_id)
    else:
        reviews = crud.review.get_provider_multi(db, current_user.provider_id)
    rating = sum([i.rating for i in reviews]) / len(reviews) if len(reviews) > 0 else 0
    return {
        'rating': round(rating, 2)
    }


@router.get('/customer_rating')
def get_customer_rating(
        *,
        db: Session = Depends(deps.get_db),
        customer_id
):
    reviews = crud.review.get_customer_multi(db, customer_id)
    rating = 0
    if reviews:
        rating = sum([i.rating for i in reviews]) / len(reviews)
    return {
        'rating': round(rating, 2)
    }


@router.get('/provider_rating')
def get_provider_rating(
        *,
        db: Session = Depends(deps.get_db),
        provider_id
):
    reviews = crud.review.get_provider_multi(db, provider_id)
    rating = 0
    if reviews:
        rating = sum([i.rating for i in reviews]) / len(reviews)
    return {
        'rating': round(rating, 2)
    }

