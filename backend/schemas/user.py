from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
import uuid

class UserBase(BaseModel):
    id: uuid.UUID
    username: str
    email: EmailStr

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str  # Plain password; will be hashed in the service

class UserRead(UserBase):
    pass

class UserAuth(BaseModel):
    username: str
    password: str

class AssetResponse(BaseModel):
    id: uuid.UUID
    name: str
    asset_type: str

    class Config:
        orm_mode = True

class UserAssetResponse(BaseModel):
    user_id: uuid.UUID
    username: str
    asset_id: uuid.UUID
    asset_name: str
    asset_type: str
    total_value: float
    average_price: float

class UserTransactionResponse(BaseModel):
    id: uuid.UUID
    asset_id: uuid.UUID
    user_id: uuid.UUID
    transaction_type: str
    amount: float
    timestamp: datetime

    class Config:
        orm_mode = True

class UserValueHistoryResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    total_value: float
    timestamp: datetime

    class Config:
        orm_mode = True


class MonthlyValueTrendResponse(BaseModel):
    time: str  # Format: 'YYYY-MM'
    value: float