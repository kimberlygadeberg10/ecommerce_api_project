# Import the Flask app from app.py
from app import app


# Test GET /users
def test_get_users():
    client = app.test_client()

    response = client.get("/users")

    assert response.status_code == 200


# Test POST /users
def test_create_user():
    client = app.test_client()

    response = client.post("/users", json={
        "name": "Test User",
        "address": "123 Test Street",
        "email": "testuser1@example.com"
    })

    assert response.status_code in [200, 201]
    assert response.get_json()["name"] == "Test User"


# Test GET /users/<id>
def test_get_user_by_id():
    client = app.test_client()

    create_response = client.post("/users", json={
        "name": "Get User Test",
        "address": "456 Test Avenue",
        "email": "getuser1@example.com"
    })

    user_id = create_response.get_json()["id"]

    response = client.get(f"/users/{user_id}")

    assert response.status_code == 200
    assert response.get_json()["id"] == user_id


# Test PUT /users/<id>
def test_update_user():
    client = app.test_client()

    create_response = client.post("/users", json={
        "name": "Old Name",
        "address": "789 Test Road",
        "email": "updateuser1@example.com"
    })

    user_id = create_response.get_json()["id"]

    response = client.put(f"/users/{user_id}", json={
        "name": "Updated Name",
        "address": "789 Test Road",
        "email": "updateuser1@example.com"
    })

    assert response.status_code == 200
    assert response.get_json()["name"] == "Updated Name"


# Test DELETE /users/<id>
def test_delete_user():
    client = app.test_client()

    create_response = client.post("/users", json={
        "name": "Delete User",
        "address": "321 Delete Lane",
        "email": "deleteuser1@example.com"
    })

    user_id = create_response.get_json()["id"]

    response = client.delete(f"/users/{user_id}")

    assert response.status_code == 200


# BONUS NEGATIVE TEST:
# Test GET /users/<id> with an ID that does not exist
def test_get_user_not_found():
    client = app.test_client()

    response = client.get("/users/999999")

    assert response.status_code == 404