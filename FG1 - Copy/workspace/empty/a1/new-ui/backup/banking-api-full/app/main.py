from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, accounts
from app.webhooks import router as webhook_router
from fastapi.responses import JSONResponse
from fastapi.requests import Request
import logging
import sys
import os

# --- Global logging setup ---
logging.basicConfig(
    filename="banking_api.log",
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(accounts.router)
app.include_router(webhook_router)

@app.get("/")
def root():
    return {"message": "Full Banking API system live"}

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)}
    )
