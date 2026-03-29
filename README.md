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