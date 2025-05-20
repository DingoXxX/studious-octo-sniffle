from fastapi import FastAPI
from app.routes import auth

app = FastAPI()
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Banking API Phase 1 is live"}
