import unittest
from uuid import uuid4
from app import app


class TestOrderRoutes(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    # Helper method to create a unique user for order tests
    def create_test_user(self):
        unique_email = f"ordertestuser_{uuid4().hex}@example.com"

        response = self.client.post("/users", json={
            "name": "Order Test User",
            "address": "123 Order Street",
            "email": unique_email
        })

        self.assertIn(response.status_code, [200, 201])

        return response.get_json()["id"]

    # Helper method to create a product for order tests
    def create_test_product(self):
        response = self.client.post("/products", json={
            "product_name": "Order Test Product",
            "price": 100.00
        })

        self.assertIn(response.status_code, [200, 201])

        return response.get_json()["id"]

    # Helper method to create an order for order tests
    def create_test_order(self):
        user_id = self.create_test_user()

        response = self.client.post("/orders", json={
            "user_id": user_id,
            "order_date": "2026-03-28T21:43:04"
        })

        self.assertIn(response.status_code, [200, 201])

        return response.get_json()["id"], user_id

    # Test POST /orders
    def test_create_order(self):
        user_id = self.create_test_user()

        response = self.client.post("/orders", json={
            "user_id": user_id,
            "order_date": "2026-03-28T21:43:04"
        })

        self.assertIn(response.status_code, [200, 201])
        self.assertEqual(response.get_json()["user_id"], user_id)

    # Test PUT /orders/<order_id>/add_product/<product_id>
    def test_add_product_to_order(self):
        order_id, user_id = self.create_test_order()
        product_id = self.create_test_product()

        response = self.client.put(
            f"/orders/{order_id}/add_product/{product_id}"
        )

        self.assertEqual(response.status_code, 200)

    # Test DELETE /orders/<order_id>/remove_product/<product_id>
    def test_remove_product_from_order(self):
        order_id, user_id = self.create_test_order()
        product_id = self.create_test_product()

        add_response = self.client.put(
            f"/orders/{order_id}/add_product/{product_id}"
        )

        self.assertEqual(add_response.status_code, 200)

        response = self.client.delete(
            f"/orders/{order_id}/remove_product/{product_id}"
        )

        self.assertEqual(response.status_code, 200)

    # Test GET /orders/user/<user_id>
    def test_get_orders_for_user(self):
        order_id, user_id = self.create_test_order()

        response = self.client.get(f"/orders/user/{user_id}")

        self.assertEqual(response.status_code, 200)

    # Test GET /orders/<order_id>/products
    def test_get_products_for_order(self):
        order_id, user_id = self.create_test_order()
        product_id = self.create_test_product()

        add_response = self.client.put(
            f"/orders/{order_id}/add_product/{product_id}"
        )

        self.assertEqual(add_response.status_code, 200)

        response = self.client.get(f"/orders/{order_id}/products")

        self.assertEqual(response.status_code, 200)

    # Negative test: POST /orders with a user ID that does not exist
    def test_create_order_with_invalid_user(self):
        response = self.client.post("/orders", json={
            "user_id": 999999,
            "order_date": "2026-03-28T21:43:04"
        })

        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
