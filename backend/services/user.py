from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from schemas.user import UserCreate, UserAuth, UserAssetResponse, UserTransactionResponse, UserValueHistoryResponse, MonthlyValueTrendResponse
from model import User, Asset, UserAsset, Transaction, ValueHistory
from utils.security import hash_password, verify_password
from typing import List, Optional
from datetime import datetime
import uuid
from fastapi import HTTPException, status
from sqlalchemy import func
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UserService:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user_create: UserCreate) -> User:
        hashed_pw = hash_password(user_create.password)


        new_user = User(
            username=user_create.username,
            email=user_create.email,
            hashed_password=hashed_pw
        )
        self.db.add(new_user)
        try:
            self.db.commit()
            self.db.refresh(new_user)
            return new_user
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username or email already exists."
            )

    def authenticate_user(self, auth_data: UserAuth) -> Optional[User]:
        user = self.db.query(User).filter(User.username == auth_data.username).first()
        if not user:
            return None
        if not verify_password(auth_data.password, user.hashed_password):
            return None
        return user

    def get_user_assets(self, user_id: uuid.UUID) -> List[UserAssetResponse]:
        user_assets = (
            self.db.query(UserAsset)
            .join(User)
            .join(Asset)
            .filter(User.id == user_id)
            .all()
        )
        result = []
        for ua in user_assets:
            result.append(UserAssetResponse(
                    user_id=ua.user.id,
                    username=ua.user.username,
                    asset_id=ua.asset.id,
                    asset_name=ua.asset.name,
                    asset_type=ua.asset.asset_type,
                    total_value=ua.total_value,
                    average_price=ua.average_price,
                    currency =ua.asset.currency
            ))

        return result


    def get_user_transactions(self, user_id: uuid.UUID) -> List[UserTransactionResponse]:
        transactions = (
            self.db.query(Transaction)
            .filter(Transaction.user_id == user_id)
            .order_by(Transaction.timestamp.desc())
            .all()
        )
        return transactions

    def get_user_value_history(
        self, 
        user_id: uuid.UUID
    ) -> List[MonthlyValueTrendResponse]:
        # Aggregate total_value by month
        query = self.db.query(
            func.date_trunc('month', ValueHistory.timestamp).label('month'),
            func.avg(ValueHistory.total_value).label('average_value')
        ).filter(
            ValueHistory.user_id == user_id
        ).group_by(
            'month'
        ).order_by(
            'month'
        )
        
        results = query.all()
        
        # Format the results for the frontend
        trend_data = [
            MonthlyValueTrendResponse(
                time=record.month.strftime("%Y-%m"),
                value=round(record.average_value, 2)
            )
            for record in results
        ]
        
        return trend_data

    def get_all_users_assets_detailed(self) -> List[UserAssetResponse]:
        user_assets = (
            self.db.query(UserAsset)
            .join(User)
            .join(Asset)
            .all()
        )
        result = []
        for ua in user_assets:
            result.append(UserAssetResponse(
                user_id=ua.user.id,
                username=ua.user.username,
                asset_id=ua.asset.id,
                asset_name=ua.asset.name,
                asset_type=ua.asset.asset_type,
                total_value=ua.total_value,
                average_price=ua.average_price
            ))
        return result
