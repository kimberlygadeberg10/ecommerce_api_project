import unittest
from uuid import uuid4
from app import app


def unique_email(prefix):
    return f"{prefix}_{uuid4().hex}@example.com"


class TestUserRoutes(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    # Test GET /users
    def test_get_users(self):
        response = self.client.get("/users")

        self.assertEqual(response.status_code, 200)

    # Test POST /users
    def test_create_user(self):
        response = self.client.post("/users", json={
            "name": "Test User",
            "address": "123 Test Street",
            "email": unique_email("testuser")
        })

        self.assertIn(response.status_code, [200, 201])
        self.assertEqual(response.get_json()["name"], "Test User")

    # Test GET /users/<id>
    def test_get_user_by_id(self):
        create_response = self.client.post("/users", json={
            "name": "Get User Test",
            "address": "456 Test Avenue",
            "email": unique_email("getuser")
        })

        self.assertIn(create_response.status_code, [200, 201])

        user_id = create_response.get_json()["id"]

        response = self.client.get(f"/users/{user_id}")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["id"], user_id)

    # Test PUT /users/<id>
    def test_update_user(self):
        create_response = self.client.post("/users", json={
            "name": "Old Name",
            "address": "789 Test Road",
            "email": unique_email("updateuser")
        })

        self.assertIn(create_response.status_code, [200, 201])

        user_id = create_response.get_json()["id"]

        response = self.client.put(f"/users/{user_id}", json={
            "name": "Updated Name",
            "address": "789 Test Road",
            "email": unique_email("updateduser")
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["name"], "Updated Name")

    # Test DELETE /users/<id>
    def test_delete_user(self):
        create_response = self.client.post("/users", json={
            "name": "Delete User",
            "address": "321 Delete Lane",
            "email": unique_email("deleteuser")
        })

        self.assertIn(create_response.status_code, [200, 201])

        user_id = create_response.get_json()["id"]

        response = self.client.delete(f"/users/{user_id}")

        self.assertEqual(response.status_code, 200)

    # Negative test: GET /users/<id> with an ID that does not exist
    def test_get_user_not_found(self):
        response = self.client.get("/users/999999")

        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()