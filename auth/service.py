from sqlalchemy.orm import Session
from fastapi import Depends

from auth.schemas import LoginInput
from auth.security import create_access_token
from mwu.db import get_db
from auth.repository import AuthRepository


class AuthService:
    def __init__(self, session: Session = Depends(get_db)):
        self.auth_service = AuthRepository(session=session)

    def login_user(self, data: LoginInput):
        user = self.auth_service.authenticate_user(data)

        token = create_access_token(data={"sub": str(user.id)})

        return {
            "access_token": token,
            "user": user
        }