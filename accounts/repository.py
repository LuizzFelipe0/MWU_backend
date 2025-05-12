from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import Session

from mwu.db import get_db
from mwu.services import ModelOperationalService
from .models import Accounts as AccountModel
from .schemas import AccountInput as AccountInScheme, AccountUpdateInput as AccountUpdateInScheme


class AccountRepository(ModelOperationalService):
    def __init__(self, session: Session = Depends(get_db)):
        super().__init__(model=AccountModel, session=session)

    def get_all_accounts(self):
        accounts = self.get_all_not_deleted()
        return accounts

    def get_deleted_accounts(self):
        accounts = self.get_all_deleted()
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
