from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import Session

from mwu.db import get_db
from mwu.repositories.operational_repositories import ModelOperationalRepository
from user_account.models import UsersAccounts
from .models import Accounts as AccountModel
from .schemas import AccountInput as AccountInScheme, AccountUpdateInput as AccountUpdateInScheme


class AccountService(ModelOperationalRepository):
    def __init__(self, session: Session = Depends(get_db)):
        super().__init__(model=AccountModel, session=session)
        self.user_accounts_service = ModelOperationalRepository(UsersAccounts, session=session)

    def get_all_accounts(self):
        accounts = self.get_all_not_deleted()
        return accounts

    def get_deleted_accounts(self):
        accounts = self.get_all_deleted()
        return accounts

    def get_accounts_by_user(self, user_id: UUID):
        user_accounts = self.user_accounts_service.get_objs_by_key(
            key="user_id",
            key_value=user_id,
            has_deleted_at=False
        )
        account_ids = [ua.account_id for ua in user_accounts]

        if not account_ids:
            return []

        accounts = (
            self.db.query(self.model)
            .filter(
                self.model.id.in_(account_ids), self.model.deleted_at.is_(None))
            .all()
        )
        return accounts

    def get_account_by_id(self, id: UUID):
        account = self.get_obj_by_id_not_deleted(obj_id=id)
        return account

    def create_account(self, data: AccountInScheme):
        account = self.create(data=data)
        return account

    def update_account(self, id: UUID, data: AccountUpdateInScheme):
        account_with_id_validated = self.get_obj_by_id_not_deleted(id)

        account = self.update(obj_id=account_with_id_validated.id, data=data)
        return account

    def delete_account(self, id: UUID):
        account_with_id_validated = self.get_obj_by_id_not_deleted(id)
        account = self.delete(obj_id=account_with_id_validated.id)
        return account

    def restore_account(self, id: UUID):
        account_with_id_validated = self.get_obj_by_id_deleted(id)
        account = self.restore(obj_id=account_with_id_validated.id)
        return account

    def force_delete_account(self, id: UUID):
        account_with_id_validated = self.get_obj_by_id_deleted(id)
        account = self.force_delete(obj_id=account_with_id_validated.id)
        return account
