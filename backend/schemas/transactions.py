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
    asset_id: Optional[uuid.UUID] = None  # Required for asset-related transactions
    amount: float = Field(..., gt=0, description="Amount must be greater than zero")

class TransactionCreate(TransactionBase):
    
    pass

class TransactionResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    asset_id: Optional[uuid.UUID]
    transaction_type: TransactionType
    amount: float
    timestamp: datetime

    class Config:
        orm_mode = True