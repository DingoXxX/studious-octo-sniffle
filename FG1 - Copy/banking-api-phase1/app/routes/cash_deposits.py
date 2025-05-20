from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime

from app.cash_deposit import CashDepositRequest, process_cash_deposit
from app.kyc_aml import check_kyc, run_aml_screening
from app.database import get_db
from app.auth import get_current_user
from app.models import Account, Transaction

router = APIRouter(prefix="/cash-deposits")

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_cash_deposit(
    deposit_request: CashDepositRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Process a physical cash deposit with required KYC/AML checks
    """
    try:
        # Run AML screening
        aml_result = run_aml_screening(current_user["full_name"])
        if aml_result["aml_flag"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Transaction requires additional review. Please visit a branch."
            )

        # Process the deposit
        result = await process_cash_deposit(
            db=db,
            user_id=current_user["id"],
            deposit_request=deposit_request
        )
        
        return result

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while processing the deposit"
        )

@router.get("/{transaction_id}")
async def get_cash_deposit_status(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Get the status of a cash deposit transaction
    """
    # Get the transaction
    transaction = db.query(Transaction).filter(
        Transaction.id == transaction_id,
        Transaction.transfer_type == "CASH_DEPOSIT"
    ).first()

    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )

    # Verify the transaction belongs to the user
    account = db.query(Account).filter(
        Account.id == transaction.account_id,
        Account.user_id == current_user["id"]
    ).first()

    if not account:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this transaction"
        )

    return {
        "transaction_id": transaction.id,
        "status": transaction.status,
        "amount": str(transaction.amount),
        "timestamp": transaction.timestamp.isoformat(),
        "location": transaction.location_id,
        "receipt_number": f"CD{transaction.id:010d}"
    }
