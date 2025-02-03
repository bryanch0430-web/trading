from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import uuid
from enum import Enum

class TransactionType(str, Enum):
    deposit = "deposit"
    withdraw = "withdraw"
    buy = "buy"
    sell = "sell"

class TransactionBase(BaseModel):
    transaction_type: TransactionType
    asset_id: Optional[uuid.UUID] = None
    amount: float = Field(..., gt=0, description="Amount must be greater than zero")

class TransactionCreate(BaseModel):
    transaction_type: TransactionType
    asset_id: Optional[uuid.UUID] 
    amount: float = Field(..., gt=0, description="Amount must be greater than zero")


class BuyTransactionCreate(BaseModel):
    buy_target_asset_id: uuid.UUID
    #use_asset_id: Optional[uuid.UUID]   # Asset used for purchasing, e.g., USD
    amount: float = Field(..., gt=0, description="Amount of asset to buy")
    user_id: uuid.UUID

class SellTransactionCreate(BaseModel):
    sell_target_asset_id: uuid.UUID
    #get_back_asset_id: Optional[uuid.UUID]   # Asset to receive, e.g., USD
    amount: float = Field(..., gt=0, description="Amount of asset to sell")
    user_id: uuid.UUID

class DepositTransactionCreate(BaseModel):
    # asset_id: Optional[uuid.UUID] 
    amount: float = Field(..., gt=0, description="Amount must be greater than zero")
    deposit_pricing: Optional[float]
    user_id: Optional[uuid.UUID] 

class WithdrawTransactionCreate(BaseModel):
    # asset_id: Optional[uuid.UUID] 
    amount: float = Field(..., gt=0, description="Amount must be greater than zero")
    user_id: Optional[uuid.UUID] 


class TransactionResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    asset_id: Optional[uuid.UUID]
    asset_name: Optional[str]
    transaction_type: TransactionType
    amount: float
    price: Optional[float]
    timestamp: datetime

    class Config:
        orm_mode = True


class UserTransactionResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    asset_id: Optional[uuid.UUID]
    transaction_type: TransactionType
    amount: float
    timestamp: datetime

    class Config:
        orm_mode = True
