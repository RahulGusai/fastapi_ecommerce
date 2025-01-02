
# FastAPI E-Commerce API

This is a RESTful API for a simple e-commerce platform, built using FastAPI.

## Features

- View available products
- Add new products
- Place orders with stock validation

## Setup

1. Install dependencies:
    ```
    pip install -r requirements.txt
    ```
2. Run the application:
    ```
    uvicorn app.main:app --reload
    ```
3. Access the API documentation at `http://127.0.0.1:8000/docs`.

## Docker

1. Build the Docker image:
    ```
    docker build -t fastapi-ecommerce .
    ```
2. Run the Docker container:
    ```
    docker run -p 80:80 fastapi-ecommerce
    ```
3. Access the API endpoints:
   ```
   http://localhost/api/products
   http://localhost/api/orders
   ```
   
