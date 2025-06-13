from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv

from .schemas import AccountOutput as AccountOutScheme, AccountInput as AccountInScheme, \
    AccountUpdateInput as AccountUpdateInScheme
from .service import AccountService

accounts_router = APIRouter(prefix="/accounts", tags=["Accounts"])


@cbv(accounts_router)
class AccountController:
    service: AccountService = Depends()

    @accounts_router.get("/all", response_model=list[AccountOutScheme | None])
    def get_all_accounts(self):
        accounts = self.service.get_all_accounts()
        return accounts

    @accounts_router.get("/deleted", response_model=list[AccountOutScheme | None])
    def get_deleted_accounts(self):
        deleted_accounts = self.service.get_deleted_accounts()
        return deleted_accounts

    @accounts_router.get("/{account_id}")
    def get_account_by_id(self, account_id: UUID) -> AccountOutScheme | None:
        account = self.service.get_account_by_id(id=account_id)
        return account

    @accounts_router.get("/{user_id}/user", response_model=list[AccountOutScheme | None])
    def get_accounts_by_user(self, user_id: UUID):
        account = self.service.get_accounts_by_user(user_id=user_id)
        return account

    @accounts_router.post("/create", response_model=AccountOutScheme, status_code=201)
    def create_account(self, data: AccountInScheme) -> AccountOutScheme:
        account = self.service.create_account(data)
        return account

    @accounts_router.patch("/{account_id}/update", status_code=200)
    def update_account(self, account_id: UUID, data: AccountUpdateInScheme) -> AccountOutScheme:
        account = self.service.update_account(id=account_id, data=data)
        return account

    @accounts_router.delete("/{account_id}/delete", status_code=200)
    def delete_account(self, account_id: UUID) -> AccountOutScheme:
        account = self.service.delete_account(id=account_id)
        return account

    @accounts_router.post("/{account_id}/restore", status_code=200)
    def restore_account(self, account_id: UUID) -> AccountOutScheme:
        account = self.service.restore_account(id=account_id)
        return account

    @accounts_router.delete("/{account_id}/force-delete", status_code=204)
    def force_delete_account(self, account_id: UUID):
        account = self.service.force_delete_account(id=account_id)
        return account
