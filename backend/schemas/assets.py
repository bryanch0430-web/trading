from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict
from datetime import datetime
import uuid
class AssetBase(BaseModel):
    name: str
    label: str
    asset_type: str


class AssetCreate(BaseModel):
    label: str

class UserAssetTypeDistribution(BaseModel):
    asset_type_values: Dict[str, float]
    total_value: float
    asset_type_percentages: Dict[str, float]

class AssetOut(BaseModel):
    id: int
    name: str
    label: str
    asset_type: str
    class Config:
        orm_mode = True


class UserAssetDisplayResponse(BaseModel):
    asset_id: uuid.UUID
    name: str
    amount: float  # total value
    average_price: float

    class Config:
        from_attributes = True

class ListUserAssetDisplayResponse(BaseModel):
    response: List[UserAssetDisplayResponse]

class ListAsset(BaseModel):
    assets: List[AssetOut]

class AssetDetails(BaseModel):
    asset_id: uuid.UUID
    name: str
    current_price: Optional[float]
    previous_close: Optional[float]
    open_price: Optional[float]
    day_high: Optional[float]
    day_low: Optional[float]
    market_cap: Optional[float]
    volume: Optional[int]
    currency: Optional[str]
    sector: Optional[str]
    industry: Optional[str]
