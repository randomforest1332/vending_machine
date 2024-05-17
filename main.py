from fastapi import FastAPI
from controllers import user, product, deposit, buy
from database import Base, engine

app = FastAPI()

# Create the database tables
Base.metadata.create_all(bind=engine)

# Include the routers
app.include_router(user.router)
app.include_router(product.router)
app.include_router(deposit.router)
app.include_router(buy.router)

@app.get("/")
def root():
    return {"message": "Welcome to the Vending Machine API"}
