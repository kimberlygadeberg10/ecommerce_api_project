# Import the Flask app from app.py
from app import app


# Test GET /products
def test_get_products():
    client = app.test_client()

    response = client.get("/products")

    assert response.status_code == 200


# Test POST /products
def test_create_product():
    client = app.test_client()

    response = client.post("/products", json={
        "product_name": "Test Laptop",
        "price": 999.99
    })

    assert response.status_code in [200, 201]
    assert response.get_json()["product_name"] == "Test Laptop"


# Test GET /products/<id>
def test_get_product_by_id():
    client = app.test_client()

    create_response = client.post("/products", json={
        "product_name": "Test Mouse",
        "price": 25.99
    })

    product_id = create_response.get_json()["id"]

    response = client.get(f"/products/{product_id}")

    assert response.status_code == 200
    assert response.get_json()["id"] == product_id


# Test PUT /products/<id>
def test_update_product():
    client = app.test_client()

    create_response = client.post("/products", json={
        "product_name": "Old Product",
        "price": 50.00
    })

    product_id = create_response.get_json()["id"]

    response = client.put(f"/products/{product_id}", json={
        "product_name": "Updated Product",
        "price": 75.00
    })

    assert response.status_code == 200
    assert response.get_json()["product_name"] == "Updated Product"


# Test DELETE /products/<id>
def test_delete_product():
    client = app.test_client()

    create_response = client.post("/products", json={
        "product_name": "Delete Product",
        "price": 10.00
    })

    product_id = create_response.get_json()["id"]

    response = client.delete(f"/products/{product_id}")

    assert response.status_code == 200


# BONUS NEGATIVE TEST:
# Test GET /products/<id> with an ID that does not exist
def test_get_product_not_found():
    client = app.test_client()

    response = client.get("/products/999999")

    assert response.status_code == 404