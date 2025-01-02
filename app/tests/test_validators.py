import pytest
from fastapi import HTTPException
from unittest.mock import MagicMock
from app.validators import validate_product_data, validate_order_items
from app.schemas import ProductCreate, OrderCreate, OrderItemBase
from app.models import Product


def test_validate_product_data_success():
    product = ProductCreate(name="Sample Product",
                            description="Test", price=10.5, stock=5)
    try:
        validate_product_data(product)
    except HTTPException:
        pytest.fail(
            "validate_product_data raised an HTTPException unexpectedly!")


def test_validate_product_data_invalid_price():
    product = ProductCreate(name="Sample Product",
                            description="Test", price=-1, stock=5)
    with pytest.raises(HTTPException) as exc_info:
        validate_product_data(product)
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Price must be greater than 0."


def test_validate_product_data_negative_stock():
    product = ProductCreate(name="Sample Product",
                            description="Test", price=10.5, stock=-1)
    with pytest.raises(HTTPException) as exc_info:
        validate_product_data(product)
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Stock cannot be negative."


def test_validate_product_data_empty_name():
    product = ProductCreate(name="  ", description="Test", price=10.5, stock=5)
    with pytest.raises(HTTPException) as exc_info:
        validate_product_data(product)
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Product name cannot be empty."


def test_validate_order_items_success():
    order = OrderCreate(products=[OrderItemBase(product_id=1, quantity=2)])
    mock_db = MagicMock()
    mock_product = Product(id=1, stock=5)
    mock_db.query.return_value.filter.return_value.first.return_value = mock_product

    try:
        product_quantities = validate_order_items(order, mock_db)
        assert product_quantities == {1: mock_product}
    except HTTPException:
        pytest.fail(
            "validate_order_items raised an HTTPException unexpectedly!")


def test_validate_order_items_product_not_found():
    order = OrderCreate(products=[OrderItemBase(product_id=1, quantity=2)])
    mock_db = MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        validate_order_items(order, mock_db)
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Product with ID 1 does not exist."


def test_validate_order_items_insufficient_stock():
    order = OrderCreate(products=[OrderItemBase(product_id=1, quantity=10)])
    mock_db = MagicMock()
    mock_product = Product(id=1, stock=5)
    mock_db.query.return_value.filter.return_value.first.return_value = mock_product

    with pytest.raises(HTTPException) as exc_info:
        validate_order_items(order, mock_db)
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == (
        "Insufficient stock for product ID 1. Available: 5, Requested: 10"
    )
