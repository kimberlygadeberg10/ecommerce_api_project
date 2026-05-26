import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_swagger_ui import get_swaggerui_blueprint
from datetime import datetime


# =========================
# APP SETUP
# =========================

app = Flask(__name__)

# Connect Flask to MySQL database
import os
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL",
    "mysql+mysqlconnector://root:Phoenix0350%23@localhost/ecommerce_api"
)
# Disable tracking modifications because it is not needed for this project
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize SQLAlchemy and Marshmallow
db = SQLAlchemy(app)
ma = Marshmallow(app)


# =========================
# SWAGGER CONFIGURATION
# =========================

SWAGGER_URL = "/api/docs"
API_URL = "/static/swagger.json"

swagger_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        "app_name": "Flask E-commerce API"
    }
)

app.register_blueprint(swagger_blueprint, url_prefix=SWAGGER_URL)


# =========================
# ASSOCIATION TABLE
# =========================
# This table connects orders and products.
# One order can have many products.
# One product can belong to many orders.
# The composite primary key prevents duplicate product/order pairs.

order_product = db.Table(
    "order_product",
    db.Column("order_id", db.Integer, db.ForeignKey("orders.id"), primary_key=True),
    db.Column("product_id", db.Integer, db.ForeignKey("products.id"), primary_key=True),
)


# =========================
# DATABASE MODELS
# =========================

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    # One user can have many orders
    orders = db.relationship("Order", backref="user", cascade="all, delete-orphan")


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_date = db.Column(db.DateTime, nullable=False)

    # Foreign key connects each order to one user
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # Many-to-many relationship between orders and products
    products = db.relationship(
        "Product",
        secondary=order_product,
        backref="orders"
    )


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)


# =========================
# MARSHMALLOW SCHEMAS
# =========================

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True


class OrderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Order
        load_instance = True
        include_fk = True


class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        load_instance = True


# Create schema instances
user_schema = UserSchema()
users_schema = UserSchema(many=True)

order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)


# =========================
# HOME ROUTE
# =========================

@app.route("/")
def home():
    return jsonify({
        "message": "Welcome to the Flask E-commerce API"
    })


# =========================
# USER ENDPOINTS
# =========================

# GET /users
@app.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return users_schema.jsonify(users), 200


# GET /users/<id>
@app.route("/users/<int:id>", methods=["GET"])
def get_user(id):
    user = User.query.get(id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    return user_schema.jsonify(user), 200


# POST /users
@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    name = data.get("name")
    address = data.get("address")
    email = data.get("email")

    if not name or not address or not email:
        return jsonify({
            "error": "Name, address, and email are required"
        }), 400

    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        return jsonify({"error": "Email already exists"}), 400

    new_user = User(
        name=name,
        address=address,
        email=email
    )

    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user), 201


# PUT /users/<id>
@app.route("/users/<int:id>", methods=["PUT"])
def update_user(id):
    user = User.query.get(id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    user.name = data.get("name", user.name)
    user.address = data.get("address", user.address)
    user.email = data.get("email", user.email)

    db.session.commit()

    return user_schema.jsonify(user), 200


# DELETE /users/<id>
@app.route("/users/<int:id>", methods=["DELETE"])
def delete_user(id):
    user = User.query.get(id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "User deleted successfully"}), 200


# =========================
# PRODUCT ENDPOINTS
# =========================

# GET /products
@app.route("/products", methods=["GET"])
def get_products():
    products = Product.query.all()
    return products_schema.jsonify(products), 200


# GET /products/<id>
@app.route("/products/<int:id>", methods=["GET"])
def get_product(id):
    product = Product.query.get(id)

    if not product:
        return jsonify({"error": "Product not found"}), 404

    return product_schema.jsonify(product), 200


# POST /products
@app.route("/products", methods=["POST"])
def create_product():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    product_name = data.get("product_name")
    price = data.get("price")

    if not product_name or price is None:
        return jsonify({
            "error": "Product name and price are required"
        }), 400

    new_product = Product(
        product_name=product_name,
        price=float(price)
    )

    db.session.add(new_product)
    db.session.commit()

    return product_schema.jsonify(new_product), 201


# PUT /products/<id>
@app.route("/products/<int:id>", methods=["PUT"])
def update_product(id):
    product = Product.query.get(id)

    if not product:
        return jsonify({"error": "Product not found"}), 404

    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    product.product_name = data.get("product_name", product.product_name)

    if "price" in data:
        product.price = float(data["price"])

    db.session.commit()

    return product_schema.jsonify(product), 200


# DELETE /products/<id>
@app.route("/products/<int:id>", methods=["DELETE"])
def delete_product(id):
    product = Product.query.get(id)

    if not product:
        return jsonify({"error": "Product not found"}), 404

    db.session.delete(product)
    db.session.commit()

    return jsonify({"message": "Product deleted successfully"}), 200


# =========================
# ORDER ENDPOINTS
# =========================

# POST /orders
@app.route("/orders", methods=["POST"])
def create_order():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    user_id = data.get("user_id")
    order_date = data.get("order_date")

    if not user_id or not order_date:
        return jsonify({
            "error": "User ID and order date are required"
        }), 400

    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    try:
        parsed_order_date = datetime.fromisoformat(order_date)
    except ValueError:
        return jsonify({
            "error": "Invalid date format. Use YYYY-MM-DDTHH:MM:SS"
        }), 400

    new_order = Order(
        user_id=user_id,
        order_date=parsed_order_date
    )

    db.session.add(new_order)
    db.session.commit()

    return order_schema.jsonify(new_order), 201


# PUT /orders/<order_id>/add_product/<product_id>
@app.route("/orders/<int:order_id>/add_product/<int:product_id>", methods=["PUT"])
def add_product_to_order(order_id, product_id):
    order = Order.query.get(order_id)
    product = Product.query.get(product_id)

    if not order:
        return jsonify({"error": "Order not found"}), 404

    if not product:
        return jsonify({"error": "Product not found"}), 404

    if product in order.products:
        return jsonify({
            "error": "Product already exists in this order"
        }), 400

    order.products.append(product)
    db.session.commit()

    return jsonify({
        "message": "Product added to order successfully"
    }), 200


# DELETE /orders/<order_id>/remove_product/<product_id>
@app.route("/orders/<int:order_id>/remove_product/<int:product_id>", methods=["DELETE"])
def remove_product_from_order(order_id, product_id):
    order = Order.query.get(order_id)
    product = Product.query.get(product_id)

    if not order:
        return jsonify({"error": "Order not found"}), 404

    if not product:
        return jsonify({"error": "Product not found"}), 404

    if product not in order.products:
        return jsonify({
            "error": "Product is not in this order"
        }), 400

    order.products.remove(product)
    db.session.commit()

    return jsonify({
        "message": "Product removed from order successfully"
    }), 200


# GET /orders/user/<user_id>
@app.route("/orders/user/<int:user_id>", methods=["GET"])
def get_orders_by_user(user_id):
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    orders = Order.query.filter_by(user_id=user_id).all()

    return orders_schema.jsonify(orders), 200


# GET /orders/<order_id>/products
@app.route("/orders/<int:order_id>/products", methods=["GET"])
def get_products_by_order(order_id):
    order = Order.query.get(order_id)

    if not order:
        return jsonify({"error": "Order not found"}), 404

    return products_schema.jsonify(order.products), 200


# =========================
# CREATE DATABASE TABLES
# =========================

with app.app_context():
    db.create_all()


# =========================
# RUN THE APP
# =========================

if __name__ == "__main__":
    app.run(debug=True)