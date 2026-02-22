from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import Session

from accounts.repository import AccountRepository
from mwu.db import get_db
from user.repository import UserRepository
from .repository import UserAccountsRepository


class UserAccountService:
    def __init__(self, session: Session = Depends(get_db)):
        self.db = session
        self.accounts_repository = AccountRepository(session=session)
        self.user_repository = UserRepository(session=session)
        self.user_accounts_repository = UserAccountsRepository(session=session)

    def get_all_user_accounts(self):
        user_accounts = self.user_accounts_repository.get_all()
        return user_accounts

    def get_user_accounts_relation_by_id(self, user_account_id: UUID):
        user_accounts_relation = self.user_accounts_repository.get_by_id(obj_id=user_account_id)
        return user_accounts_relation

    def create_user_account_relation(self, user_id: UUID, account_id: UUID):
        self.user_repository.get_by_id(obj_id=user_id)
        self.accounts_repository.get_by_id(obj_id=account_id)

        create_user_account_relation = self.user_accounts_repository.create_relation(
            user_id=user_id,
            account_id=account_id
        )
        return create_user_account_relation

    def delete_user_account_relation(self, user_id: UUID, account_id: UUID):
        delete_user_account_relation = self.user_accounts_repository.delete_relation(
            user_id=user_id,
            account_id=account_id
        )

        return delete_user_account_relation

    def get_accounts_for_user_relation(self, user_id: UUID):
        accounts_for_users = self.user_accounts_repository.get_relation_by_user(user_id=user_id)

        return accounts_for_users

    def get_users_for_account_relation(self, account_id: UUID, user_id: UUID):
        have_access = self.user_accounts_repository.get_relation(
            user_id=user_id,
            account_id=account_id
        )

        if not have_access:
            from fastapi import HTTPException
            raise HTTPException(
                status_code=403,
                detail="Access Denied: You are not allowed to access this bank account."
            )

        users_for_account = self.user_accounts_repository.get_relation_by_account(account_id=account_id)

        return users_for_account
