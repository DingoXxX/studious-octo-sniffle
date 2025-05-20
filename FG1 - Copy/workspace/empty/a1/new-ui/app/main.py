from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.exception_handlers import http_exception_handler
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from decimal import Decimal
import os
import traceback

from . import models, schemas
from .database import SessionLocal, engine
from .utils import generate_routing_number, generate_account_number
from .auth import router as auth_router
from fastapi.routing import APIRoute

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Banking API",
    description="Modern Banking API with OAuth2 and JWT authentication",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# Add CORS middleware with proper configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # React dev
        "http://localhost:8000",  # FastAPI
        "http://localhost:8080",  # Production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup templates directory
templates = Jinja2Templates(directory="app/templates")

# Mount static files (if needed later)
# app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Mount the React-based html/ folder as static
app.mount("/", StaticFiles(directory="../../html", html=True), name="frontend")

# Remove or comment out the previous catch-all route
# @app.get("/{full_path:path}", response_class=HTMLResponse)
# def serve_react_app(full_path: str):
#     index_path = os.path.join(os.path.dirname(__file__), '../../html/index.html')
#     return FileResponse(index_path)

# New catch-all for SPA, but skip docs and API routes
@app.middleware("http")
async def spa_router(request: Request, call_next):
    # Allow access to docs, openapi, redoc, and API endpoints
    if request.url.path.startswith("/docs") or \
       request.url.path.startswith("/openapi") or \
       request.url.path.startswith("/redoc") or \
       request.url.path.startswith("/api") or \
       request.url.path.startswith("/auth") or \
       request.url.path.startswith("/accounts"):
        return await call_next(request)
    # Serve React index.html for all other GET requests
    if request.method == "GET":
        index_path = os.path.join(os.path.dirname(__file__), '../../html/index.html')
        return FileResponse(index_path)
    return await call_next(request)

# Custom exception handlers
@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    # Log the error for debugging
    error_details = {
        "error": str(exc),
        "type": type(exc).__name__,
        "traceback": traceback.format_exc()
    }
    print(f"Unhandled exception: {error_details}")
    
    # Return a clean error response to the client
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred. Please try again later."}
    )

# Root route
@app.get("/")
def read_root():
    return {
        "message": "Welcome to the Banking API",
        "documentation": "/docs",
        "endpoints": {
            "create_user": "/users/",
            "get_user": "/users/{user_id}",
            "get_account": "/users/{user_id}/account",
            "deposit": "/users/{user_id}/deposit",
            "get_transactions": "/accounts/{account_id}/transactions",
            "account_page": "/account/{user_id}"
        }
    }

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        # Validate user data
        if not user.name or not user.name.strip():
            raise HTTPException(status_code=400, detail="User name must not be empty")
        
        # Check if name is too long
        if len(user.name) > 100:
            raise HTTPException(status_code=400, detail="User name is too long (max 100 characters)")
            
        # Create user
        db_user = models.User(name=user.name)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        # Create initial account with $40 balance - using the simplified schema
        account = models.Account(
            user_id=db_user.id,
            balance=40.00  # Initial $40 balance
        )
        db.add(account)
        db.commit()
        db.refresh(account)
        
        # Create initial deposit transaction
        transaction = models.Transaction(account_id=account.id, amount=40.00)
        db.add(transaction)
        db.commit()
        
        # Log successful user creation
        print(f"Created new user: {db_user.id} - {db_user.name} with account {account.id}")
        
        return db_user
        
    except HTTPException as http_ex:
        # Re-raise HTTP exceptions
        raise http_ex
    except Exception as e:
        # Log the error with full details
        error_details = {
            "error": str(e),
            "type": type(e).__name__,
            "traceback": traceback.format_exc()
        }
        print(f"Error creating user: {error_details}")
        db.rollback()  # Rollback transaction on error
        raise HTTPException(status_code=500, detail=f"Failed to create user: {str(e)}")

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.post("/users/{user_id}/link-bank")
def link_bank(user_id: int, req: schemas.LinkBankRequest, db: Session = Depends(get_db)):
    account = db.query(models.Account).filter(models.Account.user_id == user_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    # Simulate linking logic
    account.is_bank_linked = 1
    db.commit()
    db.refresh(account)
    return {"message": "Bank linked successfully", "is_bank_linked": True}

@app.post("/users/{user_id}/verify-bank")
def verify_bank(user_id: int, req: schemas.VerifyBankRequest, db: Session = Depends(get_db)):
    account = db.query(models.Account).filter(models.Account.user_id == user_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    if not account.is_bank_linked:
        raise HTTPException(status_code=400, detail="Bank must be linked first")
    # Simulate verification logic
    account.is_bank_verified = 1
    db.commit()
    db.refresh(account)
    return {"message": "Bank verified successfully", "is_bank_verified": True}

@app.post("/users/{user_id}/deposit", response_model=schemas.Account)
def deposit(user_id: int, deposit: schemas.DepositRequest, db: Session = Depends(get_db)):
    if deposit.amount <= 0:
        raise HTTPException(status_code=400, detail="Deposit amount must be positive")
    account = db.query(models.Account).filter(models.Account.user_id == user_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    # Remove bank link/verify check for simplified flow
    if not deposit.agree_terms:
        raise HTTPException(status_code=400, detail="You must agree to ACH terms and conditions")
    # Simulate processing
    account.balance += deposit.amount
    # Log transaction
    transaction = models.Transaction(
        account_id=account.id,
        amount=deposit.amount,
        transfer_type=deposit.transfer_type,
        status="pending"  # In real app, would update after processing
    )
    db.add(transaction)
    db.commit()
    db.refresh(account)
    return account

@app.get("/users/{user_id}/account", response_model=schemas.Account)
def get_account(user_id: int, db: Session = Depends(get_db)):
    account = db.query(models.Account).filter(models.Account.user_id == user_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account

@app.get("/account/{user_id}", response_class=HTMLResponse)
def get_account_page(request: Request, user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    account = db.query(models.Account).filter(models.Account.user_id == user_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    transactions = db.query(models.Transaction).filter(
        models.Transaction.account_id == account.id
    ).order_by(models.Transaction.timestamp.desc()).all()
    
    return templates.TemplateResponse(
        "account_details.html",
        {
            "request": request,
            "user_name": user.name,
            "routing_number": account.routing_number,
            "account_number": account.account_number,
            "balance": float(account.balance),
            "transactions": transactions
        }
    )

@app.get("/accounts/{account_id}/transactions", response_model=list[schemas.Transaction])
def get_transactions(account_id: int, db: Session = Depends(get_db)):
    transactions = db.query(models.Transaction).filter(models.Transaction.account_id == account_id).order_by(models.Transaction.timestamp.desc()).all()
    return transactions

from fastapi import APIRouter, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from pydantic import BaseModel
from .auth import SECRET_KEY, ALGORITHM

# Define TokenData class for JWT payload validation
class TokenData(BaseModel):
    username: str

router = APIRouter()

# JWT Security
security = HTTPBearer()

# Function to get the current user from the JWT token
def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
        
    user = db.query(models.User).filter(models.User.username == token_data.username).first()
    if user is None:
        raise credentials_exception
    return user

# New authenticated endpoints
@app.get("/users/me/account", response_model=schemas.Account)
def get_current_user_account(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    account = db.query(models.Account).filter(models.Account.user_id == current_user.id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account

@app.post("/accounts/{account_id}/deposit", response_model=schemas.Account)
def authenticated_deposit(
    account_id: int, 
    deposit_req: schemas.DepositRequest,
    current_user: models.User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    # Verify account belongs to the authenticated user
    account = db.query(models.Account).filter(
        models.Account.id == account_id,
        models.Account.user_id == current_user.id
    ).first()
    
    if not account:
        raise HTTPException(status_code=404, detail="Account not found or unauthorized")
    
    # Process deposit
    account.balance += deposit_req.amount
    
    # Create transaction record
    transaction = models.Transaction(
        account_id=account.id,
        amount=deposit_req.amount
    )
    
    db.add(transaction)
    db.commit()
    db.refresh(account)
    
    return account

app.include_router(router)
app.include_router(auth_router)
