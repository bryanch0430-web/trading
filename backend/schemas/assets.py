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


class AssetOut(BaseModel):
    id: int
    name: str
    label: str
    asset_type: str
    class Config:
        orm_mode = True


class ListAsset(BaseModel):
    assets: List[AssetOut]