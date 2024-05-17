from sqlalchemy.orm import Session
from models import Deposit

def get_deposit_by_user(db: Session, user_id: int):
    return db.query(Deposit).filter(Deposit.user_id == user_id).first()

def update_deposit(db: Session, user_id: int, amount: int):
    deposit = db.query(Deposit).filter(Deposit.user_id == user_id).first()
    if deposit:
        deposit.amount += amount
    else:
        deposit = Deposit(user_id=user_id, amount=amount)
        db.add(deposit)
    db.commit()
    db.refresh(deposit)
    return deposit
