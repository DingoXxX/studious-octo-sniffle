from fastapi import FastAPI
from app.webhooks import router as webhook_router

app = FastAPI()

app.include_router(webhook_router)

@app.get("/")
def root():
    return {"message": "Phase 3: Webhooks & License Management"}
