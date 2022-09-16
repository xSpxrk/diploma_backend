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
def get_materials(
        db: Session = Depends(deps.get_db)
):
    return crud.material.get_multi(db)