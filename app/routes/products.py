from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app import models, schemas, database

router = APIRouter()


@router.get("/products", response_model=List[schemas.ProductResponse])
def get_products(db: Session = Depends(database.get_db)):
    return db.query(models.Product).all()


@router.post("/products", response_model=schemas.ProductResponse)
def create_product(product: schemas.ProductCreate, db: Session = Depends(database.get_db)):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product
