from pydantic import BaseModel, condecimal
from datetime import datetime

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    name: str
    password: str

class UserSchema(BaseModel):
    username: str
    name: str | None = None

    class Config:
        from_attributes = True
        orm_mode = True  # For backward compatibility

class User(UserBase):
    id: int
    name: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True
        orm_mode = True  # For backward compatibility

class Deposit(BaseModel):
    amount: condecimal(max_digits=12, decimal_places=2)

class AccountBase(BaseModel):
    pass

class AccountCreate(AccountBase):
    pass

class Account(BaseModel):
    id: int
    user_id: int
    balance: condecimal(max_digits=12, decimal_places=2)
    routing_number: str
    account_number: str
    is_bank_linked: bool
    is_bank_verified: bool

    class Config:
        from_attributes = True
        orm_mode = True  # For backward compatibility

class LinkBankRequest(BaseModel):
    method: str  # e.g. 'plaid', 'manual'
    details: dict | None = None

class VerifyBankRequest(BaseModel):
    method: str  # e.g. 'micro_deposit', 'instant'
    code: str | None = None

class DepositRequest(BaseModel):
    amount: condecimal(max_digits=12, decimal_places=2)
    transfer_type: str = "Standard"  # 'Standard' by default
    agree_terms: bool = True  # True by default

class Transaction(BaseModel):
    id: int
    account_id: int
    amount: condecimal(max_digits=12, decimal_places=2)
    timestamp: datetime
    transfer_type: str | None = None
    status: str

    class Config:
        from_attributes = True
        orm_mode = True  # For backward compatibility
