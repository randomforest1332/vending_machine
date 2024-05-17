from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from schemas.product import Product, ProductCreate
from services.product import get_products, create_product, update_product
from database import get_db
from services.auth import get_current_seller_user
from models import User
from services.product import get_product_by_id, delete_product, validate_product_payload

router = APIRouter()

@router.get("/products/", response_model=List[Product])
def read_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    products = get_products(db, skip=skip, limit=limit)
    return products
  
@router.get("/products/{product_id}", response_model=Product)
def read_user(product_id: int, db: Session = Depends(get_db)):
    product = get_product_by_id(db, product_id)
    if product is None:
      raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.post("/products/", response_model=Product)
def create_new_product(product: ProductCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_seller_user)):
    validation_error = validate_product_payload(product)

    if validation_error is not None:
        raise HTTPException(status_code=400, detail=validation_error)

    created_product = create_product(db=db, product=product, user_id=current_user.id)
    return created_product
  
@router.put("/products/{product_id}", response_model=Product)
def update_existing_product(product_id: int, product: ProductCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_seller_user)):
    db_product = get_product_by_id(db, product_id=product_id)
    if product is None:
      raise HTTPException(status_code=404, detail="Product not found")
    if current_user.id != db_product.seller_id:
      raise HTTPException(status_code=403, detail="Forbidden")
    
    updated_product = update_product(db, db_product, product)
    return updated_product
  
@router.delete("/products/{product_id}", response_model=Product)
def delete_existing_product(product_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_seller_user)):
    db_product = get_product_by_id(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    if db_product.seller_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    deleted_product = delete_product(db=db, product_id=product_id)
    return deleted_product
