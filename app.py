from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)

# 🔌 Database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Pass1234%23@localhost/ecommerce_api'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 🧠 Initialize tools
db = SQLAlchemy(app)
ma = Marshmallow(app)

# 🔗 Association table (Many-to-Many)
order_product = db.Table(
    'order_product',
    db.Column('order_id', db.Integer, db.ForeignKey('order.id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True)
)

# 👤 USER MODEL
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    address = db.Column(db.String(200))
    email = db.Column(db.String(120), unique=True)

    orders = db.relationship('Order', backref='user', lazy=True)


# 🧾 ORDER MODEL
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.DateTime)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    products = db.relationship(
        'Product',
        secondary=order_product,
        backref=db.backref('orders', lazy=True)
    )


# 📦 PRODUCT MODEL
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100))
    price = db.Column(db.Float)


# 🧪 SCHEMAS
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_fk = True


class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product


class OrderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Order
        include_fk = True


# 📦 Schema instances
user_schema = UserSchema()
users_schema = UserSchema(many=True)

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)


# 👤 USER ROUTES
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify(users_schema.dump(users))


@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)

    if not user:
        return jsonify({"message": "User not found"}), 404

    return jsonify(user_schema.dump(user))


@app.route('/users', methods=['POST'])
def create_user():
    data = request.json

    new_user = User(
        name=data['name'],
        address=data['address'],
        email=data['email']
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify(user_schema.dump(new_user)), 201


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


@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)

    if not user:
        return jsonify({"message": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "User deleted"})

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


# 👋 HOME ROUTE
@app.route('/')
def home():
    return {"message": "E-commerce API is running!"}


# 🚀 RUN APP (FIXED ORDER)
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Database tables created!")

    app.run(debug=True)