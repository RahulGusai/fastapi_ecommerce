from fastapi import FastAPI
from app.routes import products, orders
from app.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(products.router, prefix="/api")
app.include_router(orders.router, prefix="/api")
