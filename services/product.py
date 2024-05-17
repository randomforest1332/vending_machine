from typing import List
from sqlalchemy.orm import Session
from models import Product
from schemas.product import ProductCreate

def get_products(db: Session, skip: int = 0, limit: int = 10) -> List[Product]:
    return db.query(Product).offset(skip).limit(limit).all()

def get_product_by_id(db: Session, product_id: int) -> Product:
    return db.query(Product).filter(Product.id == product_id).first()

def create_product(db: Session, product: ProductCreate, user_id: int):
    db_product = Product(**product.dict(), seller_id=user_id)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product
  
def update_product(db: Session, db_product: Product, product: ProductCreate):
    db_product.price = product.price
    db_product.quantity = product.quantity
    db_product.name = product.name
    db.commit()
    db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    db.delete(db_product)
    db.commit()
    return db_product
  
def validate_product_payload(product: ProductCreate):
    if product.quantity < 0:
        return "Product quantitiy should not be negative"
      
    if product.price <= 0:
        return "Product price should be more than 0"

    return None
