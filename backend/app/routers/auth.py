from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from .. import models, schemas, security
from ..database import get_db

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_pw = security.get_password_hash(user.password)
    db_user = models.User(
        name=user.name,
        email=user.email,
        hashed_password=hashed_pw,
        is_admin=user.is_admin,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = security.create_access_token(data={"sub": user.email}, expires_delta=timedelta(days=30))
    return {"access_token": access_token, "token_type": "bearer"}
