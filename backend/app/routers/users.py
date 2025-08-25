from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas
from ..database import get_db
from ..deps import get_current_admin

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=List[schemas.UserOut])
def list_users(db: Session = Depends(get_db), _: models.User = Depends(get_current_admin)):
    return db.query(models.User).all()
