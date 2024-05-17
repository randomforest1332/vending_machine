from pydantic import BaseModel
from typing import List

from schemas.product import Product

class BuyRequest(BaseModel):
    product_id: int
    product_amount: int

class BuyResponse(BaseModel):
    total_spent: float
    products: List[Product]
    change: List[int | None]
