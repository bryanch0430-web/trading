from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from schemas.user import UserCreate, UserAuth, UserAssetResponse, UserTransactionResponse, UserValueHistoryResponse,UserRead
from services.user import UserService
from utils.security import hash_password, verify_password
from typing import List, Optional
from datetime import datetime
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from database import get_db
router = APIRouter()

@router.post("/register", response_model=UserRead)
def register_user(user_create: UserCreate, db: Session = Depends(get_db)):
    service = UserService(db)
    try:
        user = service.create_user(user_create)
        return user
    except HTTPException as e:
        raise e

@router.post("/login")
def login_user(auth_data: UserAuth, db: Session = Depends(get_db)):
    service = UserService(db)
    user = service.authenticate_user(auth_data)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password."
        )
    # Here you would typically return a JWT token or some form of authentication token
    return {"message": "Authentication successful.", "user_id": user.id}


@router.get("/{user_id}/assets", response_model=List[UserAssetResponse])
def get_assets(user_id: uuid.UUID, db: Session = Depends(get_db)):
    service = UserService(db)
    assets = service.get_user_assets(user_id)
    return assets



@router.get("/{user_id}/value-history", response_model=List[UserValueHistoryResponse])
def get_value_history(
    user_id: uuid.UUID, 
    month: Optional[int] = None, 
    year: Optional[int] = None, 
    db: Session = Depends(get_db)
):
    service = UserService(db)
    try:
        history = service.get_user_value_history(user_id, month, year)
        return history
    except HTTPException as e:
        raise e