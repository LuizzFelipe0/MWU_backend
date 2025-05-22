from sqlalchemy.orm import Session
from fastapi import Depends

from auth.schemas import LoginInput
from mwu.db import get_db
from mwu.repositories.auth_repositories import AuthRepository


class AuthService:
    def __init__(self, session: Session = Depends(get_db)):
        self.auth_service = AuthRepository(session=session)

    def login_user(self, data: LoginInput):
        login = self.auth_service.authenticate_user(data)

        return login
