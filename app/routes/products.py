from typing import List
from app.validators import validate_product_data
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app import models, schemas, database

router = APIRouter()


@router.get("/products", response_model=List[schemas.ProductResponse])
def get_products(db: Session = Depends(database.get_db)):
    products = db.query(models.Product).all()
    if not products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No products found in the database."
        )
    return products


@router.post("/products", response_model=schemas.ProductResponse)
def create_product(product: schemas.ProductCreate, db: Session = Depends(database.get_db)):
    validate_product_data(product)

    try:
        db_product = models.Product(**product.dict())
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while creating the product: {str(e)}"
        )
