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
    """
    Check if any assets exist in the database and load default assets if none exist.
    """
    session = SessionLocal()
    try:
        assets_count = session.query(Asset).count()
        print('assets_count')
        if assets_count == 0:
            # Define default asset data based on your provided records.
            default_assets_data = [
                {
                    "id": "d383faea-bf2a-4a07-8fb3-294bfb31daf8",
                    "name": "USD/USD",
                    "label": "USD=X",
                    "type": "other",
                    "currency": "USD"
                },
                {
                    "id": "e799c40d-2321-498e-a6d0-59b413c82d91",
                    "name": "Bitcoin USD",
                    "label": "BTC-USD",
                    "type": "crypto",
                    "currency": "USD"


                },
                {
                    "id": "977bc0ff-2a62-4c98-90e6-443acb0286af",
                    "name": "Ethereum USD",
                    "label": "ETH-USD",
                    "type": "crypto",
                    "currency": "USD"

                },
                {
                    "id": "449a300b-bcc6-43a4-b0d5-9c605da36ab5",
                    "name": "Ethereum Name Service USD",
                    "label": "ENS-USD",
                    "type": "crypto",
                    "currency": "USD"

                },
                {
                    "id": "9fe20aca-f196-4a88-9cb0-7e406eab5653",
                    "name": "JasmyCoin USD",
                    "label": "JASMY-USD",
                    "type": "crypto",
                    "currency": "USD"

                },
                {
                    "id": "4f78f46b-97ec-4251-b73b-1bcd63e5a629",
                    "name": "Litecoin USD",
                    "label": "LTC-USD",
                    "type": "crypto",
                    "currency": "USD"

                },
                {
                    "id": "828c4121-6a90-4acb-9001-aafdafe051fd",
                    "name": "Agilent Technologies, Inc.",
                    "label": "A",
                    "type": "stock",
                    "currency": "USD"

                },
                {
                    "id": "3dfc0bb8-a4fc-465e-8644-5485ba1d9dff",
                    "name": "Visa Inc.",
                    "label": "V",
                    "type": "stock",
                    "currency": "USD"

                },
                {
                    "id": "0a4f4d00-71fe-4368-acef-765b34e422d8",
                    "name": "Alphabet Inc.",
                    "label": "GOOG",
                    "type": "stock",
                    "currency": "USD"

                },
            ]

            # Create Asset instances and add them to the session.
            default_assets = [
                Asset(
                    id=asset_data["id"],
                    name=asset_data["name"],
                    label=asset_data["label"],
                    asset_type=asset_data["type"],
                    currency = asset_data["currency"]
                )
                for asset_data in default_assets_data
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
    load_default_assets()

    start_scheduler()

if __name__ == "__main__":

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
