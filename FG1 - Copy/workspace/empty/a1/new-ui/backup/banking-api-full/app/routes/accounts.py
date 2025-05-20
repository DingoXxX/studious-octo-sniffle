from fastapi import APIRouter, Depends, HTTPException, status, Request, Body
from app.routes.auth import oauth2_scheme
from jose import jwt, JWTError
from sqlalchemy.orm import Session
import os
import logging
import time

from app.database import SessionLocal
from app.models import User, Transaction
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, ValidationError, condecimal

router = APIRouter(prefix="/accounts")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

rate_limit_store = {}
RATE_LIMIT = 5  # max 5 requests
RATE_PERIOD = 60  # per 60 seconds

# --- Logging setup ---
logger = logging.getLogger("banking_api")
logger.setLevel(logging.INFO)
handler = logging.FileHandler("banking_api.log")
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
if not logger.hasHandlers():
    logger.addHandler(handler)

class TransactionRequest(BaseModel):
    amount: float

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def check_rate_limit(username: str):
    now = int(time.time())
    window = now // RATE_PERIOD
    key = f"{username}:{window}"
    count = rate_limit_store.get(key, 0)
    if count >= RATE_LIMIT:
        raise HTTPException(status_code=429, detail="Rate limit exceeded. Try again later.")
    rate_limit_store[key] = count + 1

@router.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    token = request.headers.get("authorization", "").replace("Bearer ", "")
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username:
                check_rate_limit(username)
        except Exception:
            pass
    response = await call_next(request)
    return response

@router.get("/", dependencies=[Depends(get_current_user)])
def get_accounts(db: Session = Depends(get_db), username: str = Depends(get_current_user)):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # Example: return all accounts for the user (here, just user info)
    return {"user_id": user.id, "username": user.username}

@router.get("/balance", dependencies=[Depends(get_current_user)])
def get_balance(db: Session = Depends(get_db), username: str = Depends(get_current_user)):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # Sum all transactions for this user
    balance = db.query(Transaction).filter(Transaction.user_id == user.id).with_entities(Transaction.amount).all()
    total = sum([t[0] for t in balance]) if balance else 0.0
    return {"user_id": user.id, "balance": total}

@router.post("/transaction", dependencies=[Depends(get_current_user)])
def create_transaction(
    tx_req: TransactionRequest = Body(...),
    db: Session = Depends(get_db),
    username: str = Depends(get_current_user)
):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # Check for sufficient balance if withdrawal
    if tx_req.amount < 0:
        balance = db.query(Transaction).filter(Transaction.user_id == user.id).with_entities(Transaction.amount).all()
        total = sum([t[0] for t in balance]) if balance else 0.0
        if total + tx_req.amount < 0:
            raise HTTPException(status_code=400, detail="Insufficient funds")
    tx = Transaction(user_id=user.id, amount=tx_req.amount)
    db.add(tx)
    db.commit()
    db.refresh(tx)
    logger.info(f"User {username} initiated transaction: {tx_req.amount}")
    logger.info(f"Transaction {tx.id} completed for user {username}: {tx.amount}")
    return {"transaction_id": tx.id, "amount": tx.amount}

@router.get("/transactions", dependencies=[Depends(get_current_user)])
def get_transactions(db: Session = Depends(get_db), username: str = Depends(get_current_user)):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    txs = db.query(Transaction).filter(Transaction.user_id == user.id).all()
    logger.info(f"User {username} requested transaction history.")
    return [{"id": t.id, "amount": t.amount} for t in txs]
