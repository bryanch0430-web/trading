from fastapi import FastAPI
from routers.user import router as user_router
#, asset_router, transaction_router
from database import Base, engine, SessionLocal
from scheduler import start_scheduler  
from fastapi.middleware.cors import CORSMiddleware  
import uvicorn


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
# app.include_router(asset_router.router, prefix="/assets", tags=["Assets"])
# app.include_router(transaction_router.router, prefix="/transactions", tags=["Transactions"])



@app.get("/")
def read_root():
    return {"message": "OKOKOK"}

# initialize scheduler
@app.on_event("startup")
def on_startup():
    start_scheduler()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)