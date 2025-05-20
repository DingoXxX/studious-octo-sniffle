from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, DateTime
from sqlalchemy.sql import func
from .database import Base
import random

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    name = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    twofa_secret = Column(String, nullable=True)  # Added for 2FA
    twofa_enabled = Column(Integer, default=0, nullable=False)  # Added for 2FA (0=False, 1=True)

class Account(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    balance = Column(Numeric(12, 2), nullable=False, default=0)
    is_bank_linked = Column(Integer, nullable=False, default=0)  # 0 = False, 1 = True
    is_bank_verified = Column(Integer, nullable=False, default=0)  # 0 = False, 1 = True
    # These columns are not in the actual database, so we'll make them virtual
    # For compatibility with existing code
    @property
    def routing_number(self):
        # Generate a deterministic routing number based on the user_id
        import hashlib
        hash_obj = hashlib.md5(f"routing_{self.user_id}".encode())
        # Take first 9 digits
        return hash_obj.hexdigest()[:9]
    
    @property
    def account_number(self):
        # Generate a deterministic account number based on the account_id
        import hashlib
        hash_obj = hashlib.md5(f"account_{self.id}".encode())
        # Take first 12 digits
        return hash_obj.hexdigest()[:12]

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False, index=True)
    amount = Column(Numeric(12, 2), nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    transfer_type = Column(String, nullable=True)  # 'ACH' or 'Instant'
    status = Column(String, nullable=False, default='pending')  # 'pending', 'completed', 'failed'
