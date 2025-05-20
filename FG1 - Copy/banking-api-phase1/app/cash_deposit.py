from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, condecimal
from sqlalchemy.orm import Session

from app.models import Account, Transaction
from app.kyc import verify_identity

DEPOSIT_LIMITS = {
    "ATM": Decimal("10000.00"),  # $10,000 limit for ATM deposits
    "BRANCH": Decimal("50000.00")  # $50,000 limit for branch deposits
}

class DepositLocationType(str, Enum):
    ATM = "ATM"
    BRANCH = "BRANCH"

class IdVerificationType(str, Enum):
    DRIVERS_LICENSE = "drivers_license"
    PASSPORT = "passport"
    STATE_ID = "state_id"

class CashDepositRequest(BaseModel):
    amount: condecimal(max_digits=12, decimal_places=2, gt=0)
    deposit_location: str  # Branch/ATM location ID
    location_type: DepositLocationType
    teller_id: Optional[str] = None  # Required for branch deposits, optional for ATM
    id_verification_type: IdVerificationType
    id_document_number: str
    deposit_notes: Optional[str] = None
    source_of_funds: str  # Required for AML compliance
    
    @validator('teller_id')
    def validate_teller_id(cls, v, values):
        if values.get('location_type') == DepositLocationType.BRANCH and not v:
            raise ValueError("Teller ID is required for branch deposits")
        return v
        
    @validator('amount')
    def validate_amount(cls, v, values):
        location_type = values.get('location_type')
        if location_type and v > DEPOSIT_LIMITS[location_type]:
            raise ValueError(f"Amount exceeds {location_type.value} deposit limit of ${DEPOSIT_LIMITS[location_type]:,.2f}")
        return v

from enum import Enum
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

async def process_cash_deposit(
    db: Session,
    user_id: int,
    deposit_request: CashDepositRequest
) -> dict:
    """
    Process a physical cash deposit with required KYC/AML checks
    
    Args:
        db: Database session
        user_id: User's ID
        deposit_request: Validated deposit request
        
    Returns:
        dict: Transaction details including receipt
        
    Raises:
        ValueError: For validation errors
        Exception: For processing errors
    """
    # Check for suspicious rapid deposits
    recent_deposits = db.query(Transaction).filter(
        Transaction.account_id == user_id,
        Transaction.transfer_type == "CASH_DEPOSIT",
        Transaction.timestamp >= datetime.utcnow() - timedelta(hours=24)
    ).all()
    
    total_24h = sum(Decimal(str(tx.amount)) for tx in recent_deposits)
    if total_24h + deposit_request.amount > Decimal("10000.00"):
        logger.warning(f"High volume deposits detected for user {user_id}")
        raise ValueError("Daily deposit limit exceeded. Please visit a branch for assistance.")

    # 1. Verify user identity with enhanced logging
    try:
        kyc_result = verify_identity(str(user_id), deposit_request.id_verification_type)
        if kyc_result["status"] != "verified":
            logger.error(f"KYC verification failed for user {user_id}")
            raise ValueError("Identity verification failed")

    # 2. Get user's account
    account = db.query(Account).filter(Account.user_id == user_id).first()
    if not account:
        raise ValueError("Account not found")    # 3. Create cash deposit transaction with enhanced tracking
    verification_ref = f"{deposit_request.id_verification_type}:{deposit_request.id_document_number}"
    
    transaction = Transaction(
        account_id=account.id,
        amount=deposit_request.amount,
        transfer_type="CASH_DEPOSIT",
        status="pending",
        teller_id=deposit_request.teller_id,
        location_id=deposit_request.deposit_location,
        location_type=deposit_request.location_type,
        source_of_funds=deposit_request.source_of_funds,
        notes=deposit_request.deposit_notes,
        verification_method=deposit_request.id_verification_type,
        verification_ref=verification_ref
    )
    
    # 4. Update account balance
    account.balance += Decimal(str(deposit_request.amount))
    
    # 5. Save changes
    db.add(transaction)
    db.commit()
    db.refresh(account)
    db.refresh(transaction)

    return {
        "status": "success",
        "transaction_id": transaction.id,
        "amount": str(deposit_request.amount),
        "new_balance": str(account.balance),
        "timestamp": transaction.timestamp.isoformat(),
        "receipt_number": f"CD{transaction.id:010d}"
    }
