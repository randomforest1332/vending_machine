from pydantic import BaseModel, constr, conint, confloat

class Product(BaseModel):
    id: int
    name: str
    price: float
    quantity: int
    seller_id: int

    class Config:
        orm_mode = True
        from_attributes = True

class ProductCreate(BaseModel):
    name: constr(min_length=1)
    price: confloat(gt=0)
    quantity: conint(gt=0)
    
class ProductItem(BaseModel):
    product_id: conint(gt=0)
    quantity: conint(gt=0)
