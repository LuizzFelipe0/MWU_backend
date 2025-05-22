from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv

from .service import AuthService
from .schemas import LoginOutput, LoginInput

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@cbv(auth_router)
class AuthController:
    service: AuthService = Depends()

    @auth_router.post("/login", response_model=LoginOutput)
    def login(self, data: LoginInput):
        user = self.service.login_user(data)
        return user
