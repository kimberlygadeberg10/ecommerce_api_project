from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)

# 🔌 Database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Pass1234#@localhost/ecommerce_api'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 🧠 Initialize tools
db = SQLAlchemy(app)
order_product = db.Table(
    'order_product',
    db.Column('order_id', db.Integer, db.ForeignKey('order.id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True)
)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    address = db.Column(db.String(200))
    email = db.Column(db.String(120), unique=True)

    orders = db.relationship('Order', backref='user', lazy=True)
    class Order(db.Model):
        id = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.DateTime)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    products = db.relationship(
        'Product',
        secondary=order_product,
        lazy='subquery',
        backref=db.backref('orders', lazy=True)
    )
    class Product(db.Model):
        id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100))
    price = db.Column(db.Float)
ma = Marshmallow(app)

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
                        
user_schema = UserSchema()
users_schema = UserSchema(many=True)

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)

# 👋 Test route
@app.route('/')
def home():
    return {"message": "E-commerce API is running!"}

if __name__ == '__main__':
    app.run(debug=True)
    with app.app_context():
        db.create_all()
    print("Database tables created!")