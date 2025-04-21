import re

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def is_strong_password(password: str) -> bool:
    # Need to have strong password, 1 number, 1 Upper and 1 Lower letter, 1 number and 1 special character
    return (
            len(password) >= 8
            and bool(re.search(r"[A-Z]", password))
            and bool(re.search(r"[a-z]", password))
            and bool(re.search(r"[0-9]", password))
            and bool(re.search(r"[!@#$%^&*(),.?\":{}|<>]", password))
    )
