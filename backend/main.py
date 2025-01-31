from fastapi import FastAPI
from .routers import user_router, asset_router, transaction_router
from .database import Base, engine

# Create all database tables on startup (for demonstration only; in production,
# you may prefer to run migrations instead)
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include routers
app.include_router(user_router.router, prefix="/users", tags=["Users"])
app.include_router(asset_router.router, prefix="/assets", tags=["Assets"])
app.include_router(transaction_router.router, prefix="/transactions", tags=["Transactions"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the trading platform API"}