from sqlalchemy.orm import Session
from schemas.buy import BuyRequest
from schemas.product import Product
from schemas.deposit import Deposit

def validate_buy_request(buy_request: BuyRequest, product: Product, deposit: Deposit) -> str | None:
    if buy_request.product_amount <= 0:
        return "Product amount should be greater than 0"
      
    if product is None:
        return "Product not found"
      
    if product.quantity < buy_request.product_amount:
        return "Not enough product in stock"
    
    buy_amount = product.price * buy_request.product_amount  
    if deposit is None:
        return f"Please make a deposit of {buy_amount} to fulfill this order"
      
    if deposit.amount < buy_amount:
        return f"Deposit amount not enough. You need to deposit {buy_amount - deposit.amount} more cents to fulfill your order"

    return None
