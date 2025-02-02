from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from uuid import UUID
from datetime import datetime
from model import User, Asset, UserAsset, Transaction, ValueHistory
from schemas.transactions import TransactionCreate, TransactionResponse, TransactionType

class TransactionService:
    def __init__(self, db: Session):
        self.db = db

    def process_transaction(self, user_id: UUID, transaction_data: TransactionCreate) -> TransactionResponse:
        try:
            # Start a new transaction
            with self.db.begin():
                # Fetch the user
                user = self.db.query(User).filter(User.id == user_id).first()
                if not user:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="User not found."
                    )

                # Handle transactions that require an asset
                if transaction_data.transaction_type in [
                    TransactionType.deposit,
                    TransactionType.withdraw,
                    TransactionType.buy,
                    TransactionType.sell
                ]:
                    if not transaction_data.asset_id:
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail="asset_id is required for this transaction type."
                        )
                    
                    # Fetch the asset
                    asset = self.db.query(Asset).filter(Asset.id == transaction_data.asset_id).first()
                    if not asset:
                        raise HTTPException(
                            status_code=status.HTTP_404_NOT_FOUND,
                            detail="Asset not found."
                        )
                    
                    # Fetch or create UserAsset
                    user_asset = self.db.query(UserAsset).filter(
                        UserAsset.user_id == user_id,
                        UserAsset.asset_id == transaction_data.asset_id
                    ).first()
                    
                    if not user_asset:
                        if transaction_data.transaction_type in [TransactionType.deposit, TransactionType.buy]:
                            user_asset = UserAsset(
                                user_id=user_id,
                                asset_id=transaction_data.asset_id,
                                total_value=0.0,
                                average_price=0.0  # Assuming average_price is handled elsewhere
                            )
                            self.db.add(user_asset)
                            self.db.flush()  # Assigns an ID if needed
                        else:
                            raise HTTPException(
                                status_code=status.HTTP_400_BAD_REQUEST,
                                detail="User does not own this asset."
                            )

                    # Process based on transaction type
                    if transaction_data.transaction_type == TransactionType.deposit:
                        user_asset.total_value += transaction_data.amount
                    
                    elif transaction_data.transaction_type == TransactionType.withdraw:
                        if user_asset.total_value < transaction_data.amount:
                            raise HTTPException(
                                status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Insufficient asset balance."
                            )
                        user_asset.total_value -= transaction_data.amount
                    
                    elif transaction_data.transaction_type == TransactionType.buy:
                        # Here, you might want to deduct from user's USD/HKD balance
                        # Since USD handling isn't provided, we'll focus on asset
                        user_asset.total_value += transaction_data.amount
                    
                    elif transaction_data.transaction_type == TransactionType.sell:
                        if user_asset.total_value < transaction_data.amount:
                            raise HTTPException(
                                status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Insufficient asset balance to sell."
                            )
                        user_asset.total_value -= transaction_data.amount
                        # Here, you might want to add to user's USD/HKD balance

                # Create the Transaction record
                transaction = Transaction(
                    user_id=user_id,
                    asset_id=transaction_data.asset_id,
                    transaction_type=transaction_data.transaction_type.value,
                    amount=transaction_data.amount,
                    timestamp=datetime.utcnow()
                )
                self.db.add(transaction)

                # Update the ValueHistory
                total_value = 0.0
                for ua in user.assets:
                    total_value += ua.total_value
                value_history = ValueHistory(
                    user_id=user_id,
                    total_value=total_value,
                    timestamp=datetime.utcnow()
                )
                self.db.add(value_history)

                # Commit happens automatically with `with self.db.begin()`

                return TransactionResponse.from_orm(transaction)

        except SQLAlchemyError as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while processing the transaction."
            )