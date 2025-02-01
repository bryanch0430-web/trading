from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..schemas.user import UserCreate, UserAuth, UserAssetResponse, UserTransactionResponse, UserValueHistoryResponse
from ..model import User, Asset, UserAsset, Transaction, ValueHistory
from ..utils.security import hash_password, verify_password
from typing import List, Optional
from datetime import datetime
import uuid
from fastapi import HTTPException, status

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
                    average_price=ua.average_price
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
        user_id: uuid.UUID, 
        month: Optional[int] = None, 
        year: Optional[int] = None
    ) -> List[UserValueHistoryResponse]:
        query = self.db.query(ValueHistory).filter(ValueHistory.user_id == user_id)
        if year:
            query = query.filter(
                ValueHistory.timestamp.between(
                    datetime(year, 1, 1), 
                    datetime(year, 12, 31, 23, 59, 59)
                )
            )
        if month:
            # Ensure year is also provided when filtering by month
            if not year:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Year must be specified when filtering by month."
                )
            query = query.filter(
                ValueHistory.timestamp.between(
                    datetime(year, month, 1),
                    datetime(year, month, 28, 23, 59, 59)  # Simplistic end of month
                )
            )
        history = query.order_by(ValueHistory.timestamp.asc()).all()
        return history

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