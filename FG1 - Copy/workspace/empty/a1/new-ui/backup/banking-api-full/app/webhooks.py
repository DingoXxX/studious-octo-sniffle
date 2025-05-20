import logging
from fastapi import APIRouter, Request

logger = logging.getLogger("banking_api")
router = APIRouter(prefix="/webhooks")

@router.post("/event")
async def receive_webhook(request: Request):
    data = await request.json()
    logger.info(f"Received webhook: {data}")
    print("Received webhook:", data)
    return {"status": "received"}
