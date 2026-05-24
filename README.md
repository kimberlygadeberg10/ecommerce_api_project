🛒 E-commerce API
A RESTful API built with Flask, SQLAlchemy, Marshmallow, and MySQL to manage users, products, and orders with relational database design.

📌 Overview
This project allows you to:
Create and manage users 👤
Create and manage products 📦
Create orders for users 🧾
Add and remove products from orders 🔗

It demonstrates:
One-to-Many relationship (User → Orders)
Many-to-Many relationship (Orders ↔ Products)

⚙️ Technologies Used
Python
Flask
Flask-SQLAlchemy
Flask-Marshmallow
Marshmallow-SQLAlchemy
MySQL
MySQL Workbench
Postman

🗂 Database Structure
👤 User
id (Primary Key)
name
address
email (Unique)
📦 Product
id (Primary Key)
product_name
price
🧾 Order
id (Primary Key)
order_date
user_id (Foreign Key → User)
🔗 Order_Product (Association Table)
order_id (Foreign Key)
product_id (Foreign Key)
👉 Prevents duplicate products in an order
🚀 API Endpoints
👤 User Endpoints
GET /users → Retrieve all users
GET /users/<id> → Retrieve user by ID
POST /users → Create user
PUT /users/<id> → Update user
DELETE /users/<id> → Delete user
📦 Product Endpoints
GET /products → Retrieve all products
GET /products/<id> → Retrieve product by ID
POST /products → Create product
PUT /products/<id> → Update product
DELETE /products/<id> → Delete product
🧾 Order Endpoints
POST /orders → Create order
PUT /orders/<order_id>/add_product/<product_id> → Add product to order
DELETE /orders/<order_id>/remove_product/<product_id> → Remove product from order
GET /orders/user/<user_id> → Get orders for a user
GET /orders/<order_id>/products → Get products in an order

🧪 Testing
This API was tested using Postman.
Steps:
Create a user
Create a product
Create an order
Add product to order
Retrieve products in the order
🛠 Setup Instructions
1. Clone Repository
git clone <your-repo-url>
cd ecommerce_api_project
2. Create Virtual Environment
python3 -m venv venv
source venv/bin/activate
3. Install Dependencies
pip install Flask Flask-SQLAlchemy Flask-Marshmallow marshmallow-sqlalchemy mysql-connector-python
4. Configure Database
Update your database URI in app.py:
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:<YOUR_PASSWORD>@localhost/ecommerce_api'
5. Run the Application
python app.py
6. Test with Postman
Use the endpoints listed above to test functionality.
🎯 Features
Full CRUD operations for Users and Products
Order management system
Many-to-many relationship handling
Duplicate prevention in orders
JSON API responses
🎥 Demo
A short video demonstration was recorded showing:
API functionality
Endpoint usage
Relationship behavior
👩‍💻 Author
Kimberly Gadeberg
🏁 Final Notes
This project demonstrates how to build a fully functional REST API with relational database design, including handling complex relationships and ensuring data integrity.

## Swagger API Documentation

This project includes Swagger documentation for the Flask E-commerce API. Swagger provides a browser-based interface where users can view the available API routes, see required request data, review response formats, and understand how each endpoint works.

### Swagger URL

After starting the Flask server, open:

```txt
http://127.0.0.1:5000/api/docs

Documented Route Groups

The Swagger documentation includes routes for:

Users
Products
Orders

User Endpoints
Method	Endpoint	Description
GET	/users	Retrieve all users
GET	/users/{id}	Retrieve one user by ID
POST	/users	Create a new user
PUT	/users/{id}	Update an existing user
DELETE	/users/{id}	Delete a user

Product Endpoints
Method	Endpoint	Description
GET	/products	Retrieve all products
GET	/products/{id}	Retrieve one product by ID
POST	/products	Create a new product
PUT	/products/{id}	Update an existing product
DELETE	/products/{id}	Delete a product

Order Endpoints
Method	Endpoint	Description
POST	/orders	Create a new order for a user
PUT	/orders/{order_id}/add_product/{product_id}	Add a product to an order
DELETE	/orders/{order_id}/remove_product/{product_id}	Remove a product from an order
GET	/orders/user/{user_id}	Retrieve all orders for a specific user
GET	/orders/{order_id}/products	Retrieve all products in a specific order

Swagger Features Added
Registered a Swagger blueprint in the Flask app
Created a static/swagger.json file
Added definitions for User, Product, Order, Message, and Error responses
Added paths for all required API endpoints
Documented request bodies, path parameters, success responses, and error responses

## API Route Testing

This project includes automated route tests using Pytest. The tests are organized inside a `tests` folder, with separate test files for each major route group.

### Testing Folder Structure

```txt
tests/
├── test_users.py
├── test_products.py
└── test_orders.py

Test Files
Test File	Purpose
test_users.py	Tests all user API routes
test_products.py	Tests all product API routes
test_orders.py	Tests all order API routes
Routes Covered by Tests
User Routes
Method	Endpoint	Tested Behavior
GET	/users	Retrieves all users
POST	/users	Creates a new user
GET	/users/{id}	Retrieves a user by ID
PUT	/users/{id}	Updates an existing user
DELETE	/users/{id}	Deletes a user
GET	/users/999999	Returns 404 for a missing user
Product Routes
Method	Endpoint	Tested Behavior
GET	/products	Retrieves all products
POST	/products	Creates a new product
GET	/products/{id}	Retrieves a product by ID
PUT	/products/{id}	Updates an existing product
DELETE	/products/{id}	Deletes a product
GET	/products/999999	Returns 404 for a missing product
Order Routes
Method	Endpoint	Tested Behavior
POST	/orders	Creates a new order for an existing user
PUT	/orders/{order_id}/add_product/{product_id}	Adds a product to an order
DELETE	/orders/{order_id}/remove_product/{product_id}	Removes a product from an order
GET	/orders/user/{user_id}	Retrieves all orders for a user
GET	/orders/{order_id}/products	Retrieves all products in an order
POST	/orders with invalid user ID	Returns 404 when the user does not exist
Running Tests

Make sure the virtual environment is active:

source venv/bin/activate

Then run the full test suite:

python -m pytest

Expected result:

18 passed

Warnings may appear from SQLAlchemy or Marshmallow dependencies, but the project is considered passing as long as all tests pass.

Testing Notes

Some tests create users, products, and orders before testing routes that depend on existing data. For example, order tests first create a user because an order must belong to a valid user.

The tests use unique email addresses so repeated test runs do not fail because of duplicate user emails.

The project also includes negative tests to verify that the API correctly handles missing users, missing products, and invalid order creation.