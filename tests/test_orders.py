# Import the Flask app from app.py
from app import app

#Import uuid4 so each test user gets a unique email
from uuid import uuid4


# Helper function to create a unique user for order tests
def create_test_user(client):
    unique_email = f"ordertestuser_{uuid4().hex}@example.com"

    response = client.post("/users", json={
        "name": "Order Test User",
        "address": "123 Order Street",
        "email": unique_email
    })

    assert response.status_code in [200, 201]

    return response.get_json()["id"]


# Helper function to create a product for order tests
def create_test_product(client):
    response = client.post("/products", json={
        "product_name": "Order Test Product",
        "price": 100.00
    })

    return response.get_json()["id"]


# Helper function to create an order
def create_test_order(client):
    user_id = create_test_user(client)

    response = client.post("/orders", json={
        "user_id": user_id,
        "order_date": "2026-03-28T21:43:04"
    })

    return response.get_json()["id"], user_id


# Test POST /orders
def test_create_order():
    client = app.test_client()

    user_id = create_test_user(client)

    response = client.post("/orders", json={
        "user_id": user_id,
        "order_date": "2026-03-28T21:43:04"
    })

    assert response.status_code in [200, 201]
    assert response.get_json()["user_id"] == user_id


# Test PUT /orders/<order_id>/add_product/<product_id>
def test_add_product_to_order():
    client = app.test_client()

    order_id, user_id = create_test_order(client)
    product_id = create_test_product(client)

    response = client.put(f"/orders/{order_id}/add_product/{product_id}")

    assert response.status_code == 200


# Test DELETE /orders/<order_id>/remove_product/<product_id>
def test_remove_product_from_order():
    client = app.test_client()

    order_id, user_id = create_test_order(client)
    product_id = create_test_product(client)

    client.put(f"/orders/{order_id}/add_product/{product_id}")

    response = client.delete(f"/orders/{order_id}/remove_product/{product_id}")

    assert response.status_code == 200


# Test GET /orders/user/<user_id>
def test_get_orders_for_user():
    client = app.test_client()

    order_id, user_id = create_test_order(client)

    response = client.get(f"/orders/user/{user_id}")

    assert response.status_code == 200


# Test GET /orders/<order_id>/products
def test_get_products_for_order():
    client = app.test_client()

    order_id, user_id = create_test_order(client)
    product_id = create_test_product(client)

    client.put(f"/orders/{order_id}/add_product/{product_id}")

    response = client.get(f"/orders/{order_id}/products")

    assert response.status_code == 200


# BONUS NEGATIVE TEST:
# Test creating an order with a user ID that does not exist
def test_create_order_with_invalid_user():
    client = app.test_client()

    response = client.post("/orders", json={
        "user_id": 999999,
        "order_date": "2026-03-28T21:43:04"
    })

    assert response.status_code == 404