from datetime import UTC, datetime, timedelta

import jwt
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash

from app.core.config import settings

password_hash = PasswordHash.recommended()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def create_payload_token(user_id: int, email: str, expire_time: timedelta | None = None) -> dict[str, object]:
    if expire_time:
        expire = datetime.now(UTC) + expire_time
    else:
        expire = datetime.now(UTC) + timedelta(minutes=int(settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    payload = {'sub' : str(user_id), 'email' : email, 'exp' : expire}
    return payload

def create_access_token(payload: dict):
    encoded_jwt = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password_hash(plain_password: str, hashed_password: str,) -> bool:
    return password_hash.verify(plain_password, hashed_password,)