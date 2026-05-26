# Flask E-commerce API

## Overview

This project is a Flask-based e-commerce API that allows users, products, and orders to be created and managed. The API connects to a MySQL database and uses SQLAlchemy for the database models and relationships.

The main goal of this project was to build a working backend API with full CRUD functionality, document the API with Swagger, and test each route using Python’s built-in `unittest` library.

---

## What This Project Does

This API can:

- Create, view, update, and delete users
- Create, view, update, and delete products
- Create orders for users
- Add products to orders
- Remove products from orders
- View all orders for a user
- View all products inside an order

The project also includes Swagger documentation so the API routes are easier to understand and test.

---

## Technologies Used

- Python
- Flask
- Flask-SQLAlchemy
- Flask-Marshmallow
- Marshmallow-SQLAlchemy
- MySQL
- MySQL Connector Python
- Flask-Swagger-UI
- unittest

---

## Project Structure

```txt
ecommerce_api_project/
├── app.py
├── README.md
├── requirements.txt
├── static/
│   └── swagger.json
├── tests/
│   ├── test_users.py
│   ├── test_products.py
│   └── test_orders.py
└── venv/
Database Models

The database includes users, products, orders, and an order-product association table.

A user can have many orders. An order can have many products, and a product can belong to many orders.

Tables

The users table stores user information such as name, address, and email.

The products table stores product names and prices.

The orders table stores order dates and connects each order to a user.

The order_product table connects orders and products together for the many-to-many relationship.

API Routes
User Routes
Method	Endpoint	Description
GET	/users	Gets all users
GET	/users/{id}	Gets one user by ID
POST	/users	Creates a new user
PUT	/users/{id}	Updates a user
DELETE	/users/{id}	Deletes a user
Product Routes
Method	Endpoint	Description
GET	/products	Gets all products
GET	/products/{id}	Gets one product by ID
POST	/products	Creates a new product
PUT	/products/{id}	Updates a product
DELETE	/products/{id}	Deletes a product
Order Routes
Method	Endpoint	Description
POST	/orders	Creates a new order for a user
PUT	/orders/{order_id}/add_product/{product_id}	Adds a product to an order
DELETE	/orders/{order_id}/remove_product/{product_id}	Removes a product from an order
GET	/orders/user/{user_id}	Gets all orders for a user
GET	/orders/{order_id}/products	Gets all products in an order
Example Request Bodies
Create a User
{
  "name": "Kimberly Gadeberg",
  "address": "123 Main Street",
  "email": "kimberly@example.com"
}
Create a Product
{
  "product_name": "Laptop",
  "price": 999.99
}
Create an Order
{
  "user_id": 1,
  "order_date": "2026-03-28T21:43:04"
}
Swagger Documentation

Swagger was added to make the API easier to understand and test. It shows each endpoint, the request method, parameters, request body examples, and possible responses.

After starting the Flask server, the Swagger documentation can be viewed at:

http://127.0.0.1:5000/api/docs

The Swagger JSON file is located in:

static/swagger.json

The Swagger documentation includes routes for:

Users
Products
Orders

It also includes definitions for the expected request and response data.

Setup Instructions
1. Clone the Repository
git clone <your-repository-url>
2. Move Into the Project Folder
cd ecommerce_api_project
3. Create a Virtual Environment
python3 -m venv venv
4. Activate the Virtual Environment

Mac/Linux:

source venv/bin/activate

Windows:

venv\Scripts\activate
5. Install Dependencies
pip install -r requirements.txt
MySQL Setup

This project uses a MySQL database named:

ecommerce_api

Create the database in MySQL Workbench:

CREATE DATABASE ecommerce_api;

The database connection is configured in app.py.

Example:

app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mysql+mysqlconnector://root:YOUR_ENCODED_PASSWORD@localhost/ecommerce_api"
)

If your password has a special character like #, it needs to be encoded.

Example:

Phoenix0350# becomes Phoenix0350%23
Running the App

Make sure the virtual environment is active, then run:

python app.py

The API will run at:

http://127.0.0.1:5000

To stop the server, press:

CTRL + C
Testing

This project uses Python’s built-in unittest library.

The tests are located in the tests folder:

tests/
├── test_users.py
├── test_products.py
└── test_orders.py

Each test file focuses on one group of routes.

test_users.py tests the user routes
test_products.py tests the product routes
test_orders.py tests the order routes

To run all tests on Mac, use:

python -m unittest discover tests

A successful test run should show:

Ran 18 tests

OK
What Is Tested

The test files include at least one test for every API route.

The user tests check creating, getting, updating, and deleting users. They also include a negative test for trying to get a user that does not exist.

The product tests check creating, getting, updating, and deleting products. They also include a negative test for trying to get a product that does not exist.

The order tests check creating orders, adding products to orders, removing products from orders, getting orders for a user, and getting products in an order. They also include a negative test for trying to create an order with an invalid user ID.

Some tests create users, products, and orders first because those routes depend on data already existing in the database.

Resetting the Database During Development

If the database tables need to be reset during testing, run this in MySQL Workbench:

DROP DATABASE IF EXISTS ecommerce_api;
CREATE DATABASE ecommerce_api;

Then run the app again:

python app.py

The tables will be recreated automatically using db.create_all().

Project Status

This project is complete for the API documentation and testing assignment.

Completed items:

Created a Flask API
Connected the API to MySQL
Added SQLAlchemy models and relationships
Added Marshmallow schemas
Built user, product, and order routes
Added Swagger documentation for the API
Created a tests folder
Added separate unittest files for users, products, and orders
Added tests for every API route
Included negative tests
Updated the README with setup, testing, and usage instructions

## GitHub Actions CI Testing

This project includes a GitHub Actions workflow that automatically runs the API test suite whenever changes are pushed to the `main` branch or a pull request is opened.

The workflow is located in:

```txt
.github/workflows/main.yaml

The workflow performs the following steps:

Checks out the repository
Sets up Python
Installs project dependencies
Starts a MySQL service for testing
Runs the unittest test suite

The test command used in the workflow is:

python -m unittest discover tests

This helps make sure the API continues to work correctly when new changes are added.
