from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from services.transactions import TransactionService
from schemas.transactions import (
    BuyTransactionCreate,
    SellTransactionCreate,
    DepositTransactionCreate,
    WithdrawTransactionCreate,
    TransactionResponse,
    UserTransactionResponse
)
from database import get_db
import uuid

from typing import Optional, List

router = APIRouter()


@router.get("/transactions", response_model=List[TransactionResponse])
def get_transactions(
    user_id: uuid.UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):

    service = TransactionService(db)
    transactions = service.get_all_transactions(user_id, skip, limit)
    return transactions

@router.post("/deposit", response_model=UserTransactionResponse)
def deposit(transaction_data: DepositTransactionCreate, db: Session = Depends(get_db)):
    service = TransactionService(db)
    transaction = service.deposit(transaction_data)
    return transaction

@router.post("/withdraw", response_model=UserTransactionResponse)
def withdraw(transaction_data: WithdrawTransactionCreate, db: Session = Depends(get_db)):
    service = TransactionService(db)
    transaction = service.withdraw(transaction_data)
    return transaction

@router.post("/buy", response_model=UserTransactionResponse)
def buy(transaction_data: BuyTransactionCreate, db: Session = Depends(get_db)):
    service = TransactionService(db)
    transaction = service.buy(transaction_data)
    return transaction

@router.post("/sell", response_model=UserTransactionResponse)
def sell(transaction_data: SellTransactionCreate, db: Session = Depends(get_db)):
    service = TransactionService(db)
    transaction = service.sell(transaction_data)
    return transaction






