from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)

# 🔌 Database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Pass1234#@localhost/ecommerce_api'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 🧠 Initialize tools
db = SQLAlchemy(app)
ma = Marshmallow(app)

# 👋 Test route
@app.route('/')
def home():
    return {"message": "E-commerce API is running!"}

if __name__ == '__main__':
    app.run(debug=True)