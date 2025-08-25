from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas
from ..database import get_db
from ..deps import get_current_user

router = APIRouter(prefix="/incidents", tags=["incidents"])

@router.post("/", response_model=schemas.IncidentOut)
def create_incident(incident: schemas.IncidentCreate, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    db_incident = models.Incident(**incident.dict(), reported_by_id=user.id)
    db.add(db_incident)
    db.commit()
    db.refresh(db_incident)
    return db_incident

@router.get("/", response_model=List[schemas.IncidentOut])
def list_incidents(db: Session = Depends(get_db), _: models.User = Depends(get_current_user)):
    return db.query(models.Incident).all()
