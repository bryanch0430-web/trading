from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class AssetBase(BaseModel):
    name: str
    asset_type: str
    total_value: float

class AssetCreate(BaseModel):
    name: str
    asset_type: str
    total_value: float


class AssetOut(AssetBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True