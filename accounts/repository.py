from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session
from mwu.repositories.base_repository import BaseRepository
from .models import Accounts as AccountModel
from user_account.models import UsersAccounts as UsersAccountsModel

class AccountRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session=session, model=AccountModel)

    def _get_account_scoped_query(self, user_id: UUID, is_deleted: bool = False):
        user_accounts = self._get_query().join(
            UsersAccountsModel, self.model.id == UsersAccountsModel.account_id
        ).filter(
            UsersAccountsModel.user_id == user_id
        )

        if is_deleted:
            return user_accounts.filter(self.model.deleted_at.isnot(None))

        return user_accounts.filter(self.model.deleted_at.is_(None))

    def get_accounts_by_user(self, user_id: UUID):
        return self._get_account_scoped_query(user_id).all()

    def get_deleted_accounts_by_user(self, user_id: UUID):
        return self._get_account_scoped_query(user_id, is_deleted=True).all()

    def get_account_by_user(self, account_id: UUID, user_id: UUID):
        account = self._get_account_scoped_query(user_id).filter(
            self.model.id == account_id
        ).first()

        if not account:
            raise HTTPException(status_code=404, detail="Account not found")
        return account

    def get_deleted_account_by_user(self, account_id: UUID, user_id: UUID):
        account = self._get_account_scoped_query(user_id, is_deleted=True).filter(
            self.model.id == account_id
        ).first()

        if not account:
            raise HTTPException(status_code=404, detail="Deleted account not found")
        return account
