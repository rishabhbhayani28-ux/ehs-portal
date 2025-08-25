from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas
from ..database import get_db
from ..deps import get_current_user

router = APIRouter(prefix="/actions", tags=["actions"])

@router.post("/", response_model=schemas.ActionOut)
def create_action(action: schemas.ActionCreate, db: Session = Depends(get_db), _: models.User = Depends(get_current_user)):
    db_action = models.Action(**action.dict())
    db.add(db_action)
    db.commit()
    db.refresh(db_action)
    return db_action

@router.get("/", response_model=List[schemas.ActionOut])
def list_actions(db: Session = Depends(get_db), _: models.User = Depends(get_current_user)):
    return db.query(models.Action).all()
