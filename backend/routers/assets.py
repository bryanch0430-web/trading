from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from schemas.assets import AssetCreate, AssetDetails, UserAssetDisplayResponse,ListUserAssetDisplayResponse
from utils.security import hash_password, verify_password
from typing import List, Optional
from datetime import datetime
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from database import get_db
from services.assets import AssetService
from model import Asset, UserAsset
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

router = APIRouter()

@router.post("/create_asset", status_code=status.HTTP_201_CREATED)
def create_asset(asset: AssetCreate, db: Session = Depends(get_db)):
    service = AssetService(db)
    try:
        new_asset = service.create_asset(asset)
        return new_asset
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred.")


@router.get("/get_asset_price/{asset_id}", response_model=AssetDetails)
def get_asset_price(asset_id: uuid.UUID, db: Session = Depends(get_db)):

    service = AssetService(db)
    try:
        asset_price_details = service.get_asset_price(asset_id)
        return asset_price_details
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred.")
    

@router.get("/get_user_asset", response_model=ListUserAssetDisplayResponse)
def fetch_user_asset(user_id: uuid.UUID, db: Session = Depends(get_db)):
    service = AssetService(db)
    try:
        user_asset = service.get_user_asset(user_id)
        if not user_asset:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User asset with user_id={user_id} not found.",
            )
        return user_asset  # Return the user_asset directly
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred.",
        )
    

@router.get("/list_all_asset")
def list_all_asset( db: Session = Depends(get_db)):
    service = AssetService(db)

    try:
        assets = service.list_all_asset()

        return assets
    
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred.",
        )