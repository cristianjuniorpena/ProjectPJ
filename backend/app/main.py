from fastapi import FastAPI
from fastapi import Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.api.routes.auth import router as auth_router

from app.api.dependencies import get_db

app = FastAPI(
    title="PJ Platform API",
    description="API para intermediação de serviços PJ",
    version="1.0.0"
)
app.include_router(auth_router)

@app.get("/database-test")
def db_test(database: Session = Depends(get_db)):
    result = database.execute(
        text("SELECT current_database()")
    ).scalar_one()

    return {
        "connected": True,
        "database": result
    }

@app.get("/")
def root():
    return { "message" : "API is running"}

@app.get("/status")
def root():
    return { "status" : "healthy"}