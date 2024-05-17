from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import get_db
from models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    # Simple token validation for demonstration, ideally could be session based with JWT
    user = db.query(User).filter(User.username == token).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed",
        )
    return user

def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user is None:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def get_current_seller_user(current_user: User = Depends(get_current_active_user)):
    if current_user.role != "SELLER":
        raise HTTPException(status_code=400, detail="Not enough permissions - Role should be SELLER")
    return current_user

def get_current_buyer_user(current_user: User = Depends(get_current_active_user)):
    if current_user.role != "BUYER":
        raise HTTPException(status_code=400, detail="Not enough permissions - Role should be BUYER")
    return current_user
