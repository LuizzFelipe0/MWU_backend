from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv

from auth.utils import get_current_admin_user, get_current_user
from .schemas import UserAccountOutput as UserAccountOutScheme
from .service import UserAccountService

user_account_router = APIRouter(prefix="/users_accounts", tags=["User Account Relation"])


@cbv(user_account_router)
class UserAccountController:
    service: UserAccountService = Depends()

    @user_account_router.get("/all", response_model=list[UserAccountOutScheme])
    def get_all_user_account_relations(self, admin = Depends(get_current_admin_user)):
        account_user_relations = self.service.get_all_user_accounts()
        return account_user_relations

    @user_account_router.get("/{user_acount_id}", response_model=UserAccountOutScheme)
    def get_user_accounts_relation_by_id(self,  user_acount_id: UUID, admin = Depends(get_current_admin_user)):
        user_accounts_relation = self.service.get_user_accounts_relation_by_id(user_acount_id)
        return user_accounts_relation

    @user_account_router.get("/accounts/{user_id}/users", response_model=list[UserAccountOutScheme])
    def get_accounts_for_user(self, current_user = Depends(get_current_user)):
        account_user_relation = self.service.get_accounts_for_user_relation(user_id=current_user.id)
        return account_user_relation

    @user_account_router.get("/users/{account_id}/accounts", response_model=list[UserAccountOutScheme])
    def get_users_for_account(self, account_id: UUID, current_user = Depends(get_current_user)):
        user_account_relation = self.service.get_users_for_account_relation(account_id=account_id, user_id=current_user.id)
        return user_account_relation

    @user_account_router.post("/users/{user_id}/accounts/{account_id}", response_model=UserAccountOutScheme,
                              status_code=201)
    def create_user_account_relation(self, account_id: UUID, current_user = Depends(get_current_user)):
        user_account_relation = self.service.create_user_account_relation(user_id=current_user.id, account_id=account_id)
        return user_account_relation

    @user_account_router.delete("/users/{user_id}/accounts/{account_id}", status_code=204)
    def delete_user_account_relation(self, account_id: UUID, current_user = Depends(get_current_user)):
        user_account_relation = self.service.delete_user_account_relation(user_id=current_user.id, account_id=account_id)
        return user_account_relation
