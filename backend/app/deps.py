from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from . import models, security
from .database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = security.decode_token(token)
    if payload is None or "sub" not in payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    email: str = payload.get("sub")
    user = db.query(models.User).filter(models.User.email == email).first()
    if user is None or not user.is_active:
        raise HTTPException(status_code=401, detail="Inactive user")
    return user

def get_current_admin(user: models.User = Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admins only")
    return user
