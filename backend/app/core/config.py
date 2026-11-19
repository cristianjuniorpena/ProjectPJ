import os
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseModel):
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    ALGORITHM: str = os.getenv("ALGORITHM")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
    DUMMY_HASH: str = os.getenv("DUMMY_HASH")
settings = Settings()