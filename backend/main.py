from fastapi import FastAPI
from routers.user import router as user_router
from routers.assets import router as asset_router
from routers.transactions import router as transaction_router
#, asset_router, transaction_router
from database import Base, engine, SessionLocal
from scheduler import start_scheduler  
from fastapi.middleware.cors import CORSMiddleware  
import uvicorn
from model import Asset

Base.metadata.create_all(bind=engine)

app = FastAPI()




app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(asset_router, prefix="/assets", tags=["Assets"])
app.include_router(transaction_router, prefix="/transactions", tags=["Transactions"])



@app.get("/")
def read_root():
    return {"message": "OKOKOK"}
def load_default_assets():
    """Check if any assets exist in the database and load default assets if none exist."""
    session = SessionLocal()
    try:
        # Check if any assets are in the database
        assets_count = session.query(Asset).count()
        if assets_count == 0:
            # Define your default asset data; adjust fields as necessary
            default_assets = [
                Asset(name="Asset 1", description="Default asset 1", value=100),
                Asset(name="Asset 2", description="Default asset 2", value=200),
                # You can add further default assets here.
            ]
            session.add_all(default_assets)
            session.commit()
            print("Loaded default assets into the database.")
        else:
            print(f"Assets already exist in the database. Count: {assets_count}")
    except Exception as e:
        session.rollback()
        print("Error loading default assets:", e)
    finally:
        session.close()


# initialize scheduler
@app.on_event("startup")
def on_startup():
    start_scheduler()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)