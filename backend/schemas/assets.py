from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class AssetBase(BaseModel):
    name: str
    label: str
    asset_type: str

    
class AssetCreate(BaseModel):
    name: str
    label: str
    asset_type: str


class AssetOut(AssetBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
