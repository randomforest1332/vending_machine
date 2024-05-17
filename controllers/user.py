from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.user import User, UserCreate
from services.user import get_user_by_id, get_user_by_username, create_user, update_user, delete_user
from database import get_db
from services.auth import get_current_active_user

router = APIRouter()

@router.post("/users/", response_model=User)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    created_user = create_user(db=db, user=user)
    return created_user

@router.get("/users/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    if user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return current_user

@router.put("/users/{user_id}", response_model=User)
def update_existing_user(user_id: int, user: UserCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    db_user = get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if db_user.id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    updated_user = update_user(db=db, db_user=db_user, user=user)
    return updated_user

@router.delete("/users/{user_id}", response_model=User)
def delete_existing_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    db_user = get_user_by_id (db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if db_user.id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    deleted_user = delete_user(db=db, user_id=user_id)
    return deleted_user
