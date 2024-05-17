# Vending Machine API

## Introduction

This is a simple vending machine API built with FastAPI. It allows users with a "seller" role to manage products and users with a "buyer" role to deposit coins, buy products, and reset their deposit.

## Setup

1. Clone the repository
```
git clone <repository-url>
cd vending_machine
```
2. Install the dependencies
```
pip install -r requirements.txt
```

3. Run the application
via Docker
```
docker build -t vending_machine .
docker run -d -p 8000:8000 vending_machine
```
You should start seeing the application startup logs at `docker logs -f <container-id>`

OR

without docker
```
uvicorn main:app --reload
```

4. Access the API documentation
Open your browser and navigate to `http://127.0.0.1:8000/docs` to view and interact with the API documentation.

## Endpoints

### User Endpoints

- `POST /users/`: Create a new user
- `GET /users/`: Get a list of users
- `GET /users/{user_id}`: Get details of a specific user

### Product Endpoints

- `POST /products/`: Create a new product (Seller only)
- `GET /products/`: Get a list of products

### Deposit Endpoints

- `POST /deposit/`: Deposit coins (Buyer only)
- `GET /deposit/`: Get Deposit Detail (Buyer only)
- `POST /deposit/reset/`: Reset deposit (Buyer only)

### Buy Endpoints

- `POST /buy/`: Buy products (Buyer only)
