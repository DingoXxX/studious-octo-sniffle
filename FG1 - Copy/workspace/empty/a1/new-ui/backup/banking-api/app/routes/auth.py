from fastapi import APIRouter, Depends, HTTPException
from app.services.auth_service import authenticate_user

router = APIRouter(prefix="/auth")

@router.post("/login")
def login(username: str, password: str):
    user = authenticate_user(username, password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return {"access_token": "mocktoken", "token_type": "bearer"}
