from fastapi import APIRouter, Request

router = APIRouter(prefix="/webhooks")

@router.post("/event")
async def receive_webhook(request: Request):
    data = await request.json()
    print("Received webhook:", data)
    return {"status": "received"}
