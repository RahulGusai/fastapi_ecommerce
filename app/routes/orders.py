from app.enums import OrderStatus
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app import models, schemas, database
from app.validators import validate_order_items

router = APIRouter()


@router.post("/orders", response_model=schemas.OrderResponse)
def create_order(order: schemas.OrderCreate, db: Session = Depends(database.get_db)):
    try:
        validated_products = validate_order_items(order, db)
        print("validated")

        total_price = 0
        order_items = []

        for item in order.products:
            product = validated_products[item.product_id]
            product.stock -= item.quantity
            db.add(product)
            total_price += product.price * item.quantity

            order_item = models.OrderItem(
                product_id=product.id,
                quantity=item.quantity
            )
            order_items.append(order_item)

        db_order = models.Order(
            total_price=total_price,
            status=OrderStatus.PENDING,
            order_items=order_items
        )
        db.add(db_order)
        db.commit()
        db.refresh(db_order)
        return db_order

    except HTTPException as e:
        raise e

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while creating the order: {str(e)}"
        )
