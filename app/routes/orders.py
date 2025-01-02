from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app import models, schemas, database

router = APIRouter()


@router.post("/orders", response_model=schemas.OrderResponse)
def create_order(order: schemas.OrderCreate, db: Session = Depends(database.get_db)):
    total_price = 0
    for item in order.products:
        product = db.query(models.Product).filter(
            models.Product.id == item.product_id).first()
        if not product or product.stock < item.quantity:
            raise HTTPException(
                status_code=400, detail="Insufficient stock for product ID: {}".format(item.product_id))
        total_price += product.price * item.quantity
        product.stock -= item.quantity
        db.add(product)

    db_order = models.Order(total_price=total_price, status="completed")
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order
