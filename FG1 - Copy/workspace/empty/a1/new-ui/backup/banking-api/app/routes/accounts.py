from fastapi import APIRouter

router = APIRouter(prefix="/accounts")

@router.get("/")
def get_accounts():
    return [{"account_id": 1, "balance": 1000.0}]
