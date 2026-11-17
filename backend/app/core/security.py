from pwdlib import PasswordHash
import jwt
from jwt.exceptions import InvalidTokenError
from datetime import UTC, datetime, timedelta
from app.core.config import settings

password_hash = PasswordHash.recommended()

def create_payload_token(user_id: str, email: str, expire_time: timedelta | None = None):
    if expire_time:
        expire = datetime.now(UTC) + expire_time
    else:
        expire = datetime.now(UTC) + timedelta(int(settings.ACESS_TOKEN_EXPIRE_MINUTES))
    payload = {'sub' : user_id, 'exp' : expire}
    return payload

def create_access_token(payload: dict):
    encoded_jwt = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password_hash(plain_password: str, hashed_password: str,) -> bool:
    return password_hash.verify(plain_password, hashed_password,)