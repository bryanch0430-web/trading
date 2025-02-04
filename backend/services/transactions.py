from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from schemas.transactions import (
    BuyTransactionCreate,
    SellTransactionCreate,
    DepositTransactionCreate,
    WithdrawTransactionCreate,
    TransactionResponse
)
from model import User, Asset, UserAsset, Transaction
from datetime import datetime
import uuid
from fastapi import HTTPException, status
import logging
from typing import Optional, List
from sqlalchemy import desc
import yfinance as yf

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TransactionService:
    def __init__(self, db: Session):
        self.db = db
    def get_all_transactions(
        self, 
        user_id: uuid.UUID, 
        skip: int = 0, 
        limit: int = 100
    ) -> List["TransactionResponse"]:
        # Verify if the user exists
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Perform a join between Transaction and Asset to get asset_name
        transactions = (
            self.db.query(
                Transaction.id,
                Transaction.user_id,
                Transaction.asset_id,
                Asset.name.label("asset_name"),
                Transaction.transaction_type,
                Transaction.amount,
                Transaction.price,
                Transaction.timestamp
            )
            .join(Asset, Transaction.asset_id == Asset.id)
            .filter(Transaction.user_id == user_id)
            .order_by(desc(Transaction.timestamp))
            .offset(skip)
            .limit(limit)
            .all()
        )

        # Map the results to the TransactionResponse Pydantic model
        transaction_responses = [
            TransactionResponse(
                id=tx.id,
                user_id=tx.user_id,
                asset_id=tx.asset_id,
                asset_name=tx.asset_name,
                transaction_type=tx.transaction_type,
                amount=tx.amount,
                price=tx.price,
                timestamp=tx.timestamp,
            )
            for tx in transactions
        ]

        return transaction_responses
    def deposit(self, transaction_data: DepositTransactionCreate):
        user_id = transaction_data.user_id
        # asset_id = transaction_data.asset_id
        amount = transaction_data.amount
        label = 'USD=X'
        deposit_pricing = transaction_data.deposit_pricing
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        asset = self.db.query(Asset).filter(Asset.label == label).first()
        if not asset:
            raise HTTPException(status_code=404, detail="Asset not found")
        transaction = Transaction(
            id=uuid.uuid4(),
            user_id=user_id,
            asset_id=asset.id,
            transaction_type="deposit",
            amount=amount,
            timestamp=datetime.utcnow(),
            price = transaction_data.deposit_pricing
        )
        self.db.add(transaction)

        user_asset = self.db.query(UserAsset).filter(
            UserAsset.user_id == user_id, UserAsset.asset_id == asset.id
        ).first()
        if user_asset:
            if deposit_pricing:
                previous_total_value = user_asset.total_value
                previous_avg_price = user_asset.average_price

                new_total_value = previous_total_value + amount

                new_average_price = (
                    (previous_avg_price * previous_total_value) + (deposit_pricing * amount)
                ) / new_total_value

                user_asset.total_value = new_total_value
                user_asset.average_price = new_average_price
            else:
                user_asset.total_value += amount
        else:
            user_asset = UserAsset(
                user_id=user_id,
                asset_id=asset.id,
                total_value=amount,
                average_price=deposit_pricing if deposit_pricing else 1.0
            )
            self.db.add(user_asset)

        try:
            self.db.commit()
            self.db.refresh(transaction)
            return transaction
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=400, detail="Transaction failed")

    def withdraw(self, transaction_data: WithdrawTransactionCreate):
        user_id = transaction_data.user_id
        #asset_id = transaction_data.asset_id
        amount = transaction_data.amount
        label = 'USD=X'

        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        asset = self.db.query(Asset).filter(Asset.label == label).first()
        if not asset:
            raise HTTPException(status_code=404, detail="Asset not found")

        user_asset = self.db.query(UserAsset).filter(
            UserAsset.user_id == user_id, UserAsset.asset_id == asset.id
        ).first()
        if not user_asset or user_asset.total_value < amount:
            raise HTTPException(status_code=400, detail="Insufficient asset to withdraw")

        user_asset.total_value -= amount

        transaction = Transaction(
            user_id=user_id,
            asset_id=asset.id,
            transaction_type="withdraw",
            amount=amount,
            timestamp=datetime.utcnow()
            
        )
        self.db.add(transaction)

        try:
            self.db.commit()
            self.db.refresh(transaction)
            return transaction
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=400, detail="Transaction failed")

    def buy(self, transaction_data: BuyTransactionCreate):
        user_id = transaction_data.user_id
        buy_target_asset_id = transaction_data.buy_target_asset_id
        amount = transaction_data.amount
        label = 'USD=X'

        # Validate user exists
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Validate target asset exists
        target_asset = self.db.query(Asset).filter(Asset.id == buy_target_asset_id).first()
        if not target_asset:
            raise HTTPException(status_code=404, detail="Target asset not found")

        # Fetch current buying price using yfinance
        try:
            stock = yf.Ticker(target_asset.label)
            data = stock.history(period="1d")
            if data.empty:
                raise ValueError("No data retrieved for the asset.")
            current_buying_price = float(data['Close'].iloc[-1])  # Convert to native Python float
        except Exception as e:
            print(str(e))
            raise HTTPException(status_code=400, detail=f"Failed to retrieve current price: {str(e)}")

        # Validate use_asset exists (e.g., USD)
        use_asset = self.db.query(Asset).filter(Asset.label == label).first()
        if not use_asset:
            raise HTTPException(status_code=404, detail="Use asset not found")

        # Check that the user has sufficient funds
        total_cost = float(amount * current_buying_price)  # Convert to native Python float
        user_use_asset = self.db.query(UserAsset).filter(
            UserAsset.user_id == user_id, UserAsset.asset_id == use_asset.id
        ).first()
        if not user_use_asset or user_use_asset.total_value < total_cost:
            raise HTTPException(status_code=400, detail="Insufficient funds to perform this transaction")

        # Deduct the total cost from user's use_asset
        user_use_asset.total_value = float(user_use_asset.total_value - total_cost)  # Convert to native Python float

        # Update or create user's target asset holdings
        user_target_asset = self.db.query(UserAsset).filter(
            UserAsset.user_id == user_id, UserAsset.asset_id == buy_target_asset_id
        ).first()
        if user_target_asset:
            previous_total_value = float(user_target_asset.total_value)
            previous_avg_price = float(user_target_asset.average_price)

            new_total_value = float(previous_total_value + amount)
            new_average_price = float(
                (previous_avg_price * previous_total_value) + (current_buying_price * amount)
            ) / new_total_value

            user_target_asset.total_value = new_total_value
            user_target_asset.average_price = new_average_price
        else:
            # Create new UserAsset record
            user_target_asset = UserAsset(
                user_id=user_id,
                asset_id=buy_target_asset_id,
                total_value=float(amount),
                average_price=float(current_buying_price),
            )
            self.db.add(user_target_asset)

        # Create a Transaction record
        transaction = Transaction(
            user_id=user_id,
            asset_id=buy_target_asset_id,
            transaction_type="buy",
            amount=float(amount),
            timestamp=datetime.utcnow(),
            price=float(current_buying_price)  # Ensure price is a native Python float
        )
        self.db.add(transaction)

        try:
            self.db.commit()
            self.db.refresh(transaction)
            return transaction
        except Exception as e:
            print(str(e))
            self.db.rollback()
            raise HTTPException(status_code=400, detail=f"Transaction failed: {str(e)}")


    def sell(self, transaction_data: SellTransactionCreate):
        user_id = transaction_data.user_id
        sell_target_asset_id = transaction_data.sell_target_asset_id
        amount = transaction_data.amount
        label = 'USD=X'

        # Validate user exists
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Validate target asset exists
        target_asset = self.db.query(Asset).filter(Asset.id == sell_target_asset_id).first()
        if not target_asset:
            raise HTTPException(status_code=404, detail="Target asset not found")

        # Fetch current selling price using yfinance
        try:
            stock = yf.Ticker(target_asset.label)
            data = stock.history(period="1d")
            if data.empty:
                raise ValueError("No data retrieved for the asset.")
            current_selling_price = float(data['Close'].iloc[-1])  # Convert to native Python float
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to retrieve current price: {str(e)}")

        # Validate get_back_asset exists (e.g., USD)
        get_back_asset = self.db.query(Asset).filter(Asset.label == label).first()
        if not get_back_asset:
            raise HTTPException(status_code=404, detail="Get back asset not found")

        # Check that the user has sufficient asset to sell
        user_target_asset = self.db.query(UserAsset).filter(
            UserAsset.user_id == user_id, UserAsset.asset_id == sell_target_asset_id
        ).first()
        if not user_target_asset or user_target_asset.total_value < amount:
            raise HTTPException(status_code=400, detail="Insufficient asset to sell")

        # Calculate new total value and average price for the target asset
        previous_total_value = float(user_target_asset.total_value)
        previous_average_price = float(user_target_asset.average_price)
        total_value_after = float(previous_total_value - amount)

        # Calculate proceeds from the sale
        proceeds = float(amount * current_selling_price)  # Convert to native Python float

        # Update user's target asset holdings
        user_target_asset.total_value = total_value_after
        if total_value_after > 0:
            user_target_asset.average_price = previous_average_price
        else:
            user_target_asset.average_price = 0.0

        # Update or create user's get_back_asset holdings (e.g., USD)
        user_get_back_asset = self.db.query(UserAsset).filter(
            UserAsset.user_id == user_id, UserAsset.asset_id == get_back_asset.id
        ).first()
        if user_get_back_asset:
            user_get_back_asset.total_value = float(user_get_back_asset.total_value + amount) 
             #user_get_back_asset.average_price = # Convert to native Python float
        else:
            user_get_back_asset = UserAsset(
                user_id=user_id,
                asset_id=get_back_asset.id,
                total_value=float(amount),  # Convert to native Python float
                average_price=1.0  # USD to USD only
            )
            self.db.add(user_get_back_asset)

        # Create a Transaction record
        transaction = Transaction(
            user_id=user_id,
            asset_id=sell_target_asset_id,
            transaction_type="sell",
            amount=float(amount),  # Convert to native Python float
            timestamp=datetime.utcnow(),
            price=float(current_selling_price)  # Convert to native Python float
        )
        self.db.add(transaction)

        try:
            self.db.commit()
            self.db.refresh(transaction)
            return transaction
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=400, detail=f"Transaction failed: {str(e)}")
        


        

