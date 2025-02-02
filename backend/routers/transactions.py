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
router = APIRouter()



