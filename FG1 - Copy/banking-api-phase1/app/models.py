from sqlalchemy import Column, Integer, String, DateTime, Numeric, ForeignKey, func, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True)
    full_name = Column(String(100))
    hashed_password = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Account(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    balance = Column(Numeric(12, 2), nullable=False, default=0)
    routing_number = Column(String(9))  # Standard 9-digit ABA routing number
    account_number = Column(String(12))  # Up to 12 digits for account number
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_active = Column(Integer, default=1)
    kyc_status = Column(String(20), default="pending")  # pending, verified, rejected
    last_kyc_check = Column(DateTime(timezone=True))

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False, index=True)
    amount = Column(Numeric(12, 2), nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    transfer_type = Column(String(20), nullable=False)  # CASH_DEPOSIT, ACH, WIRE, etc.
    status = Column(String(20), nullable=False, default="pending")
    teller_id = Column(String(50))  # For cash deposits
    location_id = Column(String(50))  # Branch/ATM location
    source_of_funds = Column(String(100))  # For AML compliance
    notes = Column(Text)
    verification_method = Column(String(50))  # ID verification method used
    verification_ref = Column(String(100))  # Reference number of verification
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
