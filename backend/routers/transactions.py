from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from services.transactions import TransactionService
from schemas.transactions import (
    BuyTransactionCreate,
    SellTransactionCreate,
    DepositTransactionCreate,
    WithdrawTransactionCreate,
    TransactionResponse,
)
from database import get_db

router = APIRouter()

@router.post("/deposit", response_model=TransactionResponse)
def deposit(transaction_data: DepositTransactionCreate, db: Session = Depends(get_db)):
    service = TransactionService(db)
    transaction = service.deposit(transaction_data)
    return transaction

@router.post("/withdraw", response_model=TransactionResponse)
def withdraw(transaction_data: WithdrawTransactionCreate, db: Session = Depends(get_db)):
    service = TransactionService(db)
    transaction = service.withdraw(transaction_data)
    return transaction

@router.post("/buy", response_model=TransactionResponse)
def buy(transaction_data: BuyTransactionCreate, db: Session = Depends(get_db)):
    service = TransactionService(db)
    transaction = service.buy(transaction_data)
    return transaction

@router.post("/sell", response_model=TransactionResponse)
def sell(transaction_data: SellTransactionCreate, db: Session = Depends(get_db)):
    service = TransactionService(db)
    transaction = service.sell(transaction_data)
    return transaction