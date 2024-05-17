from sqlalchemy.orm import Session
from models import User
from schemas.user import UserCreate

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def create_user(db: Session, user: UserCreate):
    db_user = User(username=user.username, password=user.password, name=user.name, role=user.role.value)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
  
def update_user(db: Session, db_user: User, user: UserCreate):
    db_user.username = user.username
    db_user.password = user.password
    db_user.role = user.role.value
    db_user.name = user.name
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()
    db.delete(db_user)
    db.commit()
    return db_user

