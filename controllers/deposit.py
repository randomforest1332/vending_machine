from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.deposit import Deposit
from services.deposit import get_deposit_by_user, update_deposit
from database import get_db
from services.auth import get_current_buyer_user
from models import User

router = APIRouter()

@router.get("/deposit/", response_model=Deposit)
def get_deposit_for_user(db: Session = Depends(get_db), current_user: User = Depends(get_current_buyer_user)):
    user_deposit = get_deposit_by_user(db, user_id=current_user.id)
    return user_deposit


@router.post("/deposit/", response_model=Deposit)
def deposit_coins(deposit: Deposit, db: Session = Depends(get_db), current_user: User = Depends(get_current_buyer_user)):
    if deposit.amount not in [5, 10, 20, 50, 100]:
        raise HTTPException(status_code=400, detail="Invalid coin denomination")
    updated_deposit = update_deposit(db=db, user_id=current_user.id, amount=deposit.amount)
    return updated_deposit

@router.post("/deposit/reset")
def reset_deposit(db: Session = Depends(get_db), current_user: User = Depends(get_current_buyer_user)):
    deposit = get_deposit_by_user(db, current_user.id)
    deposit_amount = deposit.amount
    if deposit:
        deposit.amount = 0
        db.commit()
    return {"message": "Deposit reset", "previous_amount": deposit_amount}
