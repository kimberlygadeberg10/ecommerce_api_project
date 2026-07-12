# Flask E-commerce API

## Project Overview

The Flask E-commerce API is a RESTful web service built with Flask that manages users, products, and orders for a simple e-commerce system. The API demonstrates CRUD operations, relational database design, API documentation with Swagger, automated testing, continuous integration/deployment with GitHub Actions, and cloud deployment using Render.

---

## Live Deployment

**Live API:**

https://ecommerce-api-project.onrender.com

**Swagger Documentation:**

https://ecommerce-api-project.onrender.com/api/docs/

---

## GitHub Repository

https://github.com/kimberlygadeberg10/ecommerce_api_project

---

## Features

- User Management
  - Create users
  - View all users
  - View individual users
  - Update users
  - Delete users

- Product Management
  - Create products
  - View all products
  - View individual products
  - Update products
  - Delete products

- Order Management
  - Create orders
  - View customer orders
  - Add products to orders
  - Remove products from orders
  - View products within an order

- Interactive Swagger API documentation

- PostgreSQL database hosted on Render

- Automated testing using Python unittest

- Continuous Integration and Deployment using GitHub Actions

---

## Technologies Used

- Python 3
- Flask
- Flask SQLAlchemy
- Flask Marshmallow
- Marshmallow
- MySQL Connector (Local Development)
- PostgreSQL (Production)
- Gunicorn
- Swagger UI
- GitHub Actions
- Render
- unittest

---

## Installation

Clone the repository:

```bash
git clone https://github.com/kimberlygadeberg10/ecommerce_api_project.git
```

Navigate into the project folder:

```bash
cd ecommerce_api_project
```

Create a virtual environment:

```bash
python3 -m venv venv
```

Activate the virtual environment:

macOS/Linux

```bash
source venv/bin/activate
```

Windows

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the project root.

Example:

```text
DATABASE_URL=your_database_url
SECRET_KEY=your_secret_key
```

---

## Running the Application

Start the Flask application locally:

```bash
gunicorn flask_app:app
```

The application will be available at:

```
http://127.0.0.1:8000
```

---

## Running Tests

Run all unit tests:

```bash
python -m unittest discover tests
```

---

## API Endpoints

### Users

| Method | Endpoint |
|----------|----------------|
| GET | /users |
| GET | /users/<id> |
| POST | /users |
| PUT | /users/<id> |
| DELETE | /users/<id> |

---

### Products

| Method | Endpoint |
|----------|----------------|
| GET | /products |
| GET | /products/<id> |
| POST | /products |
| PUT | /products/<id> |
| DELETE | /products/<id> |

---

### Orders

| Method | Endpoint |
|----------|----------------------------------------------|
| POST | /orders |
| GET | /orders/user/<user_id> |
| GET | /orders/<order_id>/products |
| PUT | /orders/<order_id>/add_product/<product_id> |
| DELETE | /orders/<order_id>/remove_product/<product_id> |

---

## Deployment

The application is deployed on Render using:

- Render Web Service
- Render PostgreSQL Database
- Gunicorn
- Environment Variables
- GitHub Actions CI/CD Pipeline

---

## CI/CD Pipeline

GitHub Actions automatically:

- Builds the project
- Installs dependencies
- Runs all unit tests
- Deploys to Render after tests pass successfully

---

## Project Structure

```
ecommerce_api_project/
│
├── .github/
│   └── workflows/
│       └── main.yaml
│
├── static/
│   └── swagger.json
│
├── tests/
│   ├── test_users.py
│   ├── test_products.py
│   └── test_orders.py
│
├── flask_app.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Author

Kimberly Gadeberg

GitHub:

https://github.com/kimberlygadeberg10

---

## License

This project was created for educational purposes as part of a Software Engineering curriculum.