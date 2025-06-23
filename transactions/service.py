from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import Session

from accounts.models import Accounts as AccountModel
from categories.models import Category as CategoryModel
from mwu.db import get_db
from mwu.repositories.operational_repositories import ModelOperationalRepository
from user.models import User as UserModel
from .models import Transactions as TransactionModel
from .schemas import TransactionInput as TransactionInScheme, TransactionUpdateInput as TransactionUpdateInScheme


class TransactionsService(ModelOperationalRepository):
    def __init__(self, session: Session = Depends(get_db)):
        super().__init__(model=TransactionModel, session=session)
        self.account_service = ModelOperationalRepository(AccountModel, session=session)
        self.category_service = ModelOperationalRepository(CategoryModel, session=session)
        self.user_service = ModelOperationalRepository(UserModel, session=session)

    def get_all_transactions(self):
        transactions = self.get_all_not_deleted()
        return transactions

    def get_deleted_transactions(self):
        transactions = self.get_all_deleted()
        return transactions

    def get_transaction_by_id(self, id: UUID):
        transaction = self.get_obj_by_id_not_deleted(obj_id=id)
        return transaction

    def get_transaction_by_user(self, user_id: UUID):
        transaction = self.get_objs_by_key(key="user_id", key_value=user_id)
        return transaction

    def create_transaction(self, data: TransactionInScheme):  # Need to implement next_due_date rule
        self.user_service.get_obj_by_id_not_deleted(obj_id=data.user_id)
        self.category_service.get_obj_by_id_not_deleted(obj_id=data.category_id)

        if data.account_id is not None:
            self.account_service.get_obj_by_id_not_deleted(obj_id=data.account_id)

        transaction = self.create(data=data)
        return transaction

    def update_transaction(self, id: UUID, data: TransactionUpdateInScheme):
        transaction_with_id_validated = self.get_obj_by_id_not_deleted(id)

        if data.user_id is not None:
            self.user_service.get_obj_by_id_not_deleted(data.user_id)
        elif data.category_id is not None:
            self.category_service.get_obj_by_id(data.category_id)

        transaction = self.update(obj_id=transaction_with_id_validated.id, data=data)
        return transaction

    def delete_transaction(self, id: UUID):
        transaction_with_id_validated = self.get_obj_by_id_not_deleted(id)
        transaction = self.delete(obj_id=transaction_with_id_validated.id)
        return transaction

    def restore_transaction(self, id: UUID):
        transaction_with_id_validated = self.get_obj_by_id_deleted(id)
        transaction = self.restore(obj_id=transaction_with_id_validated.id)
        return transaction

    def force_delete_transaction(self, id: UUID):
        transaction_with_id_validated = self.get_obj_by_id_deleted(id)
        transaction = self.force_delete(obj_id=transaction_with_id_validated.id)
        return transaction
