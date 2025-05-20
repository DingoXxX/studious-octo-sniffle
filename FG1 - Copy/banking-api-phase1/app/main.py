from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import os

from app.database import engine, Base
from app.routes import auth, accounts, cash_deposits
from app.models import User, Account, Transaction

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Banking API",
    description="Secure API for banking operations including cash deposits",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL", "http://localhost:3000")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(accounts.router, prefix="/accounts", tags=["Accounts"])
app.include_router(cash_deposits.router, prefix="/cash-deposits", tags=["Cash Deposits"])
