from fastapi import HTTPException, status
from app.schemas import ProductCreate, OrderCreate
from sqlalchemy.orm import Session
from app import models


def validate_product_data(product: ProductCreate):
    if product.price <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Price must be greater than 0."
        )
    if product.stock < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Stock cannot be negative."
        )
    if not product.name.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product name cannot be empty."
        )


def validate_order_items(order: OrderCreate, db: Session):
    """
    Validate if the products in the order exist and have sufficient stock.
    """
    product_quantities = {}
    for item in order.products:
        product = db.query(models.Product).filter(
            models.Product.id == item.product_id).first()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with ID {item.product_id} does not exist."
            )
        if product.stock < item.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    f"Insufficient stock for product ID {item.product_id}. "
                    f"Available: {product.stock}, Requested: {item.quantity}"
                )

            )
        product_quantities[product.id] = product
    return product_quantities
