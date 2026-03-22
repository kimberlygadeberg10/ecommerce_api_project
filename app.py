from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime

# =========================
# 🚀 APP SETUP
# =========================

app = Flask(__name__)

# 🔌 Connect Flask to MySQL database
# %23 = encoded "#" in password
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Pass1234%23@localhost/ecommerce_api'

# 🚫 Disable tracking modifications (saves memory, not needed for this project)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 🧠 Initialize database (SQLAlchemy) and serialization tool (Marshmallow)
db = SQLAlchemy(app)
ma = Marshmallow(app)

# =========================
# 🔗 MANY-TO-MANY TABLE
# =========================
# This table connects Orders and Products
# One order can have many products, and one product can appear in many orders

order_product = db.Table(
    'order_product',
    db.Column('order_id', db.Integer, db.ForeignKey('order.id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True)
)

# =========================
# 👤 USER MODEL
# =========================
# Represents customers using the system

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    address = db.Column(db.String(200))
    email = db.Column(db.String(120), unique=True)

    # One user can have many orders
    orders = db.relationship('Order', backref='user', lazy=True)

# =========================
# 📦 PRODUCT MODEL
# =========================
# Represents items that can be ordered

class Product(db.Model):
    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100))
    price = db.Column(db.Float)

# =========================
# 🧾 ORDER MODEL
# =========================
# Represents a purchase made by a user

class Order(db.Model):
    __tablename__ = 'order'

    id = db.Column(db.Integer, primary_key=True)

    # Automatically stores the time order is created
    order_date = db.Column(db.DateTime, default=datetime.utcnow)

    # Links order to a user
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # Many-to-many relationship with products
    products = db.relationship(
        'Product',
        secondary=order_product,
        backref=db.backref('orders', lazy=True)
    )

# =========================
# 🧪 MARSHMALLOW SCHEMAS
# =========================
# These convert Python objects → JSON and validate output

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User  # tells schema which model to use


class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product


class OrderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Order
        include_fk = True  # ensures foreign keys like user_id are included

# Create schema instances
user_schema = UserSchema()
users_schema = UserSchema(many=True)

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)

# =========================
# 👤 USER ROUTES (CRUD)
# =========================

# GET all users
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify(users_schema.dump(users))

# GET single user by ID
@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    return jsonify(user_schema.dump(user))

# CREATE user
@app.route('/users', methods=['POST'])
def create_user():
    data = request.json  # get JSON from Postman

    new_user = User(
        name=data['name'],
        address=data['address'],
        email=data['email']
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify(user_schema.dump(new_user)), 201

# UPDATE user
@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get(id)

    if not user:
        return jsonify({"message": "User not found"}), 404

    data = request.json

    user.name = data.get('name', user.name)
    user.address = data.get('address', user.address)
    user.email = data.get('email', user.email)

    db.session.commit()

    return jsonify(user_schema.dump(user))

# DELETE user
@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)

    if not user:
        return jsonify({"message": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "User deleted"})

# =========================
# 📦 PRODUCT ROUTES (CRUD)
# =========================

@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify(products_schema.dump(products))

@app.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get(id)

    if not product:
        return jsonify({"message": "Product not found"}), 404

    return jsonify(product_schema.dump(product))

@app.route('/products', methods=['POST'])
def create_product():
    data = request.json

    new_product = Product(
        product_name=data['product_name'],
        price=data['price']
    )

    db.session.add(new_product)
    db.session.commit()

    return jsonify(product_schema.dump(new_product)), 201

@app.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get(id)

    if not product:
        return jsonify({"message": "Product not found"}), 404

    data = request.json

    product.product_name = data.get('product_name', product.product_name)
    product.price = data.get('price', product.price)

    db.session.commit()

    return jsonify(product_schema.dump(product))

@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)

    if not product:
        return jsonify({"message": "Product not found"}), 404

    db.session.delete(product)
    db.session.commit()

    return jsonify({"message": "Product deleted"})

# =========================
# 🧾 ORDER ROUTES
# =========================

# GET all orders
@app.route('/orders', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    return jsonify(orders_schema.dump(orders))

# GET single order by ID
@app.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = Order.query.get(order_id)

    if not order:
        return jsonify({"message": "Order not found"}), 404

    return jsonify(order_schema.dump(order))

# CREATE order
@app.route('/orders', methods=['POST'])
def create_order():
    data = request.json

    user = User.query.get(data['user_id'])

    if not user:
        return jsonify({"message": "User not found"}), 404

    new_order = Order(
        order_date=datetime.utcnow(),
        user_id=data['user_id']
    )

    db.session.add(new_order)
    db.session.commit()

    return jsonify(order_schema.dump(new_order)), 201

# ADD product to order (many-to-many relationship)
@app.route('/orders/<int:order_id>/add_product/<int:product_id>', methods=['PUT'])
def add_product_to_order(order_id, product_id):
    order = Order.query.get(order_id)
    product = Product.query.get(product_id)

    if not order or not product:
        return jsonify({"message": "Order or Product not found"}), 404

    if product in order.products:
        return jsonify({"message": "Product already in order"}), 400

    order.products.append(product)
    db.session.commit()

    return jsonify({"message": "Product added to order"})

# REMOVE product from order
@app.route('/orders/<int:order_id>/remove_product/<int:product_id>', methods=['DELETE'])
def remove_product_from_order(order_id, product_id):
    order = Order.query.get(order_id)
    product = Product.query.get(product_id)

    if not order or not product:
        return jsonify({"message": "Order or Product not found"}), 404

    if product not in order.products:
        return jsonify({"message": "Product not in order"}), 400

    order.products.remove(product)
    db.session.commit()

    return jsonify({"message": "Product removed from order"})

# GET all orders for a specific user
@app.route('/orders/user/<int:user_id>', methods=['GET'])
def get_orders_by_user(user_id):
    orders = Order.query.filter_by(user_id=user_id).all()
    return jsonify(orders_schema.dump(orders))

# GET all products in an order
@app.route('/orders/<int:order_id>/products', methods=['GET'])
def get_products_in_order(order_id):
    order = Order.query.get(order_id)

    if not order:
        return jsonify({"message": "Order not found"}), 404

    return jsonify(products_schema.dump(order.products))

# =========================
# 🏠 HOME ROUTE
# =========================

@app.route('/')
def home():
    return {"message": "E-commerce API is running!"}

# =========================
# 🚀 RUN APP
# =========================

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # creates tables if they don't exist
        print("Database tables created!")

    app.run(debug=True)

# 🧪 TEST ROUTE (for Postman debugging)
@app.route('/test', methods=['POST'])
def test():
    return {"message": "POST works"}