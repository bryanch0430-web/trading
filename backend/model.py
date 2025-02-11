from sqlalchemy import Column, String, Float, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    transactions = relationship("Transaction", back_populates="user")
    assets = relationship("UserAsset", back_populates="user")
    value_history = relationship("ValueHistory", back_populates="user")

class Asset(Base):
    __tablename__ = "assets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, index=True, nullable=False)
    label = Column(String, index=True, nullable=False)
    asset_type = Column(String, nullable=False)  # e.g., "crypto", "stock", ...
    currency = Column(String, nullable=False) 
    user_assets = relationship("UserAsset", back_populates="asset")
    transactions = relationship("Transaction", back_populates="asset")

class UserAsset(Base):
    __tablename__ = "user_assets"

    # Composite primary key (user_id, asset_id)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    asset_id = Column(UUID(as_uuid=True), ForeignKey("assets.id"), primary_key=True)
    total_value = Column(Float, default=0.0, nullable=False)
    average_price = Column(Float, default=0.0, nullable=False)

    user = relationship("User", back_populates="assets")
    asset = relationship("Asset", back_populates="user_assets")

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    asset_id = Column(UUID(as_uuid=True), ForeignKey("assets.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    transaction_type = Column(String, nullable=False)  # deposit, withdraw, buy, sell
    amount = Column(Float, nullable=False)
    price = Column(Float, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="transactions")
    asset = relationship("Asset", back_populates="transactions")

class ValueHistory(Base):
    __tablename__ = "value_history"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), index=True, nullable=False)
    total_value = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="value_history")
