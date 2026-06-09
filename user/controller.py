from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv
from sqlalchemy.sql.functions import current_user

from auth.utils import get_current_admin_user, get_current_user
from .service import UserService
from .schemas import UserOutput as UserOutScheme, UserInput as UserInScheme, UserUpdateInput as UserUpdateInScheme


users_router = APIRouter(prefix="/users", tags=["Users"])


@cbv(users_router)
class UserController:
    service: UserService = Depends()

    @users_router.get("/all", response_model=list[UserOutScheme | None])
    def get_all_users(self, admin = Depends(get_current_admin_user)):
        users = self.service.get_all_users()
        return users

    @users_router.get("/deleted", response_model=list[UserOutScheme | None])
    def get_deleted_users(self, admin = Depends(get_current_admin_user)):
        deleted_users = self.service.get_deleted_users()
        return deleted_users

    @users_router.get("/{user_id}", response_model=UserOutScheme)
    def get_user_by_id(self, user_id: UUID, current_user = Depends(get_current_user)):
        user = self.service.get_user_by_id(id=user_id, requester=current_user)
        return user

    @users_router.post("/create", response_model=UserOutScheme, status_code=201)
    def create_user(self, data: UserInScheme) -> UserOutScheme:
        user = self.service.create_user(data)
        return user

    @users_router.patch("/{user_id}/update", status_code=200 , response_model=UserOutScheme)
    def update_user(self, user_id: UUID, data: UserUpdateInScheme, current_user = Depends(get_current_user)) -> UserOutScheme:
        user = self.service.update_user(id=user_id, data=data, requester=current_user)
        return user

    @users_router.delete("/{user_id}/delete", status_code=200)
    def delete_user(self, user_id: UUID, current_user = Depends(get_current_user)) -> UserOutScheme:
        user = self.service.delete_user(id=user_id, requester=current_user)
        return user

    @users_router.post("/{user_id}/restore", status_code=200)
    def restore_user(self, user_id: UUID, admin = Depends(get_current_admin_user)) -> UserOutScheme:
        user = self.service.restore_user(id=user_id)
        return user

    @users_router.delete("/{user_id}/force-delete", status_code=204)
    def force_delete_user(self, user_id: UUID, admin = Depends(get_current_admin_user)):
        user = self.service.force_delete_user(id=user_id)
        return user