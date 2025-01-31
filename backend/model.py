from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)


    transactions = relationship("Transaction", back_populates="user")
    assets = relationship("UserAsset", back_populates="user")
    value_history = relationship("ValueHistory", back_populates="user")


class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    asset_type = Column(String)  # e.g. "crypto", "stock", ...

    user_assets = relationship("UserAsset", back_populates="asset")


class UserAsset(Base):
    __tablename__ = "user_assets"

    # Composite primary key (user_id, asset_id)
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    asset_id = Column(Integer, ForeignKey("assets.id"), primary_key=True)

    total_value = Column(Float, default=0.0)

    user = relationship("User", back_populates="assets")
    asset = relationship("Asset", back_populates="user_assets")


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("assets.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    transaction_type = Column(String)  
    amount = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="transactions")



class ValueHistory(Base):
    __tablename__ = "value_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    total_value = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="value_history")