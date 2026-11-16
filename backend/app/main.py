from fastapi import FastAPI
from fastapi import Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.api.routes.auth_router import router as auth_router
from app.api.routes.user_router import router as user_router

from app.api.dependencies import get_database

app = FastAPI(
    title="PJ Platform API",
    description="API para intermediação de serviços PJ",
    version="1.0.0"
)
app.include_router(auth_router)
app.include_router(user_router)

@app.get("/database-test")
def database_test(database: Session = Depends(get_database)):
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