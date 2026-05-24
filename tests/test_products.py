import unittest
from app import app


class TestProductRoutes(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    # Test GET /products
    def test_get_products(self):
        response = self.client.get("/products")

        self.assertEqual(response.status_code, 200)

    # Test POST /products
    def test_create_product(self):
        response = self.client.post("/products", json={
            "product_name": "Test Laptop",
            "price": 999.99
        })

        self.assertIn(response.status_code, [200, 201])
        self.assertEqual(response.get_json()["product_name"], "Test Laptop")

    # Test GET /products/<id>
    def test_get_product_by_id(self):
        create_response = self.client.post("/products", json={
            "product_name": "Test Mouse",
            "price": 25.99
        })

        self.assertIn(create_response.status_code, [200, 201])

        product_id = create_response.get_json()["id"]

        response = self.client.get(f"/products/{product_id}")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["id"], product_id)

    # Test PUT /products/<id>
    def test_update_product(self):
        create_response = self.client.post("/products", json={
            "product_name": "Old Product",
            "price": 50.00
        })

        self.assertIn(create_response.status_code, [200, 201])

        product_id = create_response.get_json()["id"]

        response = self.client.put(f"/products/{product_id}", json={
            "product_name": "Updated Product",
            "price": 75.00
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["product_name"], "Updated Product")

    # Test DELETE /products/<id>
    def test_delete_product(self):
        create_response = self.client.post("/products", json={
            "product_name": "Delete Product",
            "price": 10.00
        })

        self.assertIn(create_response.status_code, [200, 201])

        product_id = create_response.get_json()["id"]

        response = self.client.delete(f"/products/{product_id}")

        self.assertEqual(response.status_code, 200)

    # Negative test: GET /products/<id> with an ID that does not exist
    def test_get_product_not_found(self):
        response = self.client.get("/products/999999")

        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()