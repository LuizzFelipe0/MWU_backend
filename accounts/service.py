from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import Session

from mwu.db import get_db
from user_account.repository import UserAccountsRepository
from .repository import AccountRepository
from .schemas import AccountInput as AccountInScheme, AccountUpdateInput as AccountUpdateInScheme


class AccountService:
    def __init__(self, session: Session = Depends(get_db)):
        self.account_repository = AccountRepository(session=session)
        self.user_accounts_repository = UserAccountsRepository(session=session)

    def get_all_accounts(self, user_id: UUID):
        accounts = self.account_repository.get_accounts_by_user(user_id=user_id)
        return accounts

    def get_deleted_accounts(self, user_id: UUID):
        deleted_accounts = self.account_repository.get_deleted_accounts_by_user(user_id=user_id)
        return deleted_accounts

    def get_account_by_id(self, id: UUID, user_id: UUID):
        account = self.account_repository.get_account_by_user(
            account_id=id,
            user_id=user_id
        )
        return account

    def create_account(self, data: AccountInScheme, user_id: UUID):
        account = self.account_repository.create(data=data)

        self.user_accounts_repository.create_relation( # Automatically creates row in user_accounts table
            user_id=user_id,
            account_id=account.id
        )

        return account

    def update_account(self, id: UUID, data: AccountUpdateInScheme, user_id: UUID):
        self.account_repository.get_account_by_user(account_id=id, user_id=user_id)

        account = self.account_repository.update(obj_id=id, data=data)
        return account

    def delete_account(self, id: UUID, user_id: UUID):
        account_validated = self.account_repository.get_account_by_user(
            account_id=id,
            user_id=user_id
        )
        account = self.account_repository.soft_delete(obj_id=account_validated.id)
        return account

    def restore_account(self, id: UUID, user_id: UUID):
        deleted_account = self.account_repository.get_deleted_account_by_user(
            account_id=id,
            user_id=user_id
        )
        account = self.account_repository.restore(obj_id=deleted_account.id)
        return account

    def force_delete_account(self, id: UUID, user_id: UUID):
        deleted_account = self.account_repository.get_deleted_account_by_user(
            account_id=id,
            user_id=user_id
        )
        self.user_accounts_repository.delete_relation(  # Automatically deletes row in user_accounts table
            user_id=user_id,
            account_id=deleted_account.id
        )

        account = self.account_repository.force_delete(obj_id=deleted_account.id)

        return account
