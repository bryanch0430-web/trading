from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from schemas.assets import AssetCreate
from utils.security import hash_password, verify_password
from typing import List, Optional
from datetime import datetime
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from database import get_db
from services.assets import AssetService
from model import Asset
router = APIRouter()

@router.post("/fetchStock")
def fetch_stock(db: Session = Depends(get_db)):
    service = AssetService(db)
    try:
        a = service.import_assets_from_csv()
        return a
    except HTTPException as e:
        raise e
# @router.get("/list_all_asset",response_model=[Asset])