from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from schemas.user import UserCreate, UserAuth, UserAssetResponse, UserTransactionResponse, UserValueHistoryResponse,UserRead,MonthlyValueTrendResponse, Token, TokenData
from services.user import UserService
from utils.security import hash_password, verify_password,create_access_token
from typing import List, Optional
from datetime import datetime, timedelta
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from database import get_db
from model import User
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token")

SECRET_KEY = "SECRET_KEY"  
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> "User":
    """
    Dependency to get the current user from the JWT token.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except jwt.PyJWTError:
        raise credentials_exception
    user = db.query(User).filter(User.username == token_data.username).first()
    if user is None:
        raise credentials_exception
    return user
@router.post("/register", response_model=UserRead)
def register_user(user_create: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter((User.username == user_create.username) | (User.email == user_create.email)).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username or email already registered")
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



@router.get("/{user_id}/value-history", response_model=List[MonthlyValueTrendResponse])
def get_value_history(
    user_id: uuid.UUID, 
    db: Session = Depends(get_db)
):
    service = UserService(db)
    try:
        history = service.get_user_value_history(user_id)
        return history
    except HTTPException as e:
        raise e


@router.post("/token", response_model=Token)
def login_for_access_token(auth_data: UserAuth, db: Session = Depends(get_db)):
    """
    User login endpoint. It authenticates the user and returns a JWT token.
    """
    service = UserService(db)
    user = service.authenticate_user(auth_data)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> "User":
    """
    Dependency to get the current user from the JWT token.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except jwt.PyJWTError:
        raise credentials_exception
    user = db.query(User).filter(User.username == token_data.username).first()
    if user is None:
        raise credentials_exception
    return user

@router.get("/me")
def read_users_me(current_user: "User" = Depends(get_current_user)):
    """
    Retrieve the current logged-in user's information.
    """
    return current_user
