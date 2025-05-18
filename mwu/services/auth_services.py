from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from auth.schemas import LoginInput
from auth.security import verify_password
from user.models import User as UserModel


class AuthService:
    def __init__(self, session: Session):
        self.db = session

    def authenticate_user(self, data: LoginInput) -> UserModel:
        user = self.db.query(UserModel).filter_by(email=data.email, deleted_at=None).first()

        if not user or not verify_password(data.password, user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        return user
