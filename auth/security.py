import os
import re
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import HTTPException
from passlib.context import CryptContext
from cryptography.fernet import Fernet

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")
cipher_suite = Fernet(ENCRYPTION_KEY.encode())

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_field(field: str) -> str:
    return pwd_context.hash(field)


def encrypt_field(value: str) -> str:
    if not value:
        return value
    return cipher_suite.encrypt(value.encode()).decode()


def decrypt_field(value: str) -> str:
    if not value:
        return value
    try:
        return cipher_suite.decrypt(value.encode()).decode()
    except Exception:
        return value


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


def is_strong_password(password: str) -> bool:
    # Need to have strong password, 1 number, 1 Upper and 1 Lower letter, 1 number and 1 special character
    strong_password = (
            len(password) >= 8
            and bool(re.search(r"[A-Z]", password))
            and bool(re.search(r"[a-z]", password))
            and bool(re.search(r"[0-9]", password))
            and bool(re.search(r"[!@#$%^&*(),.?\":{}|<>]", password))
    )

    if not strong_password:
        raise HTTPException(status_code=422, detail="This Password is not valid, Try Again!")

    return strong_password
