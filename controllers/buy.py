from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.buy import BuyRequest, BuyResponse
from schemas.product import Product as ProductSchema
from services.deposit import get_deposit_by_user
from services.buy import validate_buy_request
from database import get_db
from services.auth import get_current_buyer_user
from models import User
from services.product import get_product_by_id

router = APIRouter()

@router.post("/buy/", response_model=BuyResponse)
def buy_products(buy_request: BuyRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_buyer_user)):
    product = get_product_by_id(db, buy_request.product_id)
    deposit = get_deposit_by_user(db, current_user.id)
    
    validation_error = validate_buy_request(buy_request, product, deposit)
    
    if validation_error is not None:
        raise HTTPException(status_code=400, detail=validation_error)
    
    
    total_cost = product.price * buy_request.product_amount

    product.quantity -= buy_request.product_amount
    deposit.amount -= total_cost
    db.commit()

    change = calculate_change(deposit.amount)
    deposit.amount = 0
    db.commit()
    
    print(f"{total_cost} {[product]} {change}")
    
    purchased_product = ProductSchema.from_orm(product)

    return BuyResponse(total_spent=total_cost, products=[purchased_product], change=change)

def calculate_change(amount):
    coins = [100, 50, 20, 10, 5]
    change = []
    for coin in coins:
        while amount >= coin:
            amount -= coin
            change.append(coin)
    return change
