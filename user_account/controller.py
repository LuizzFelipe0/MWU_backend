from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv

from .repository import UserAccountRepository
from .schemas import UserAccountOutput as UserAccountOutScheme

user_account_router = APIRouter(prefix="/users_acounts", tags=["User Account Relation"])


@cbv(user_account_router)
class UserAccountController:
    service: UserAccountRepository = Depends()

    @user_account_router.get("/users/{user_id}/accounts", response_model=list[UserAccountOutScheme])
    def get_accounts_for_user(self, user_id: UUID):
        account_user_relation = self.service.get_accounts_for_user_relation(user_id=user_id)
        return account_user_relation

    @user_account_router.get("/accounts/{account_id}/users", response_model=list[UserAccountOutScheme])
    def get_users_for_account(self, account_id: UUID):
        user_account_relation = self.service.get_users_for_account_relation(account_id=account_id)
        return user_account_relation

    @user_account_router.post("/users/{user_id}/accounts/{account_id}", response_model=UserAccountOutScheme,
                              status_code=201)
    def create_user_account_relation(self, user_id: UUID, account_id: UUID):
        user_account_relation = self.service.create_user_account_relation(user_id=user_id, account_id=account_id)
        return user_account_relation

    @user_account_router.delete("/users/{user_id}/accounts/{account_id}", status_code=204)
    def delete_user_account_relation(self, user_id: UUID, account_id: UUID):
        user_account_relation = self.service.delete_user_account_relation(user_id=user_id, account_id=account_id)
        return user_account_relation
