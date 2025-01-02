import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Test cases for Products


@pytest.fixture
def product_data():
    return {"name": "Sample Product", "description": "A test product", "price": 20.5, "stock": 15}


def test_create_product(product_data):
    response = client.post("/api/products/", json=product_data)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["name"] == product_data["name"]
    assert response_data["description"] == product_data["description"]
    assert response_data["price"] == product_data["price"]
    assert response_data["stock"] == product_data["stock"]
    assert "id" in response_data


def test_get_products():
    response = client.get("/api/products/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


# Test cases for Orders
@pytest.fixture
def order_data(product_data):
    product_response = client.post("/api/products/", json=product_data)
    product_id = product_response.json()["id"]
    return {"products": [{"product_id": product_id, "quantity": 3}]}


def test_create_order(order_data):
    response = client.post("/api/orders/", json=order_data)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["status"] == "pending"
    assert response_data["total_price"] > 0
    assert "id" in response_data
    assert "order_items" in response_data
