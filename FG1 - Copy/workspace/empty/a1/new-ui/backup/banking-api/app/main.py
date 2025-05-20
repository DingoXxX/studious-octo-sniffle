from fastapi import FastAPI
from app.routes import auth, accounts

app = FastAPI()

app.include_router(auth.router)
app.include_router(accounts.router)

@app.get("/")
def root():
    return {"message": "Banking API is live"}
