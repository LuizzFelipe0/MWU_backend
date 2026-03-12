from typing import Optional
from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import Session

from accounts.repository import AccountRepository
from categories.repository import CategoryRepository
from category_types.repository import CategoryTypeRepository
from mwu.db import get_db

from .repository import TransactionsRepository
from .schemas import TransactionInput as TransactionInScheme, TransactionUpdateInput as TransactionUpdateInScheme


class TransactionsService:
    def __init__(self, session: Session = Depends(get_db)):
        self.transactions_repository = TransactionsRepository(session)
        self.account_repository = AccountRepository(session)
        self.category_repository = CategoryRepository(session)
        self.category_type_repository = CategoryTypeRepository(session)


    def get_all_transactions(self, user_id: UUID):
        transactions = self.transactions_repository.get_transactions_by_user(user_id=user_id)
        return transactions

    def get_deleted_transactions(self, user_id: UUID):
        transactions = self.transactions_repository.get_deleted_transactions_by_user(user_id=user_id)
        return transactions

    def get_transaction_by_id(self, id: UUID, user_id: UUID):
        transaction = self.transactions_repository.get_transaction_by_user(
            transaction_id=id,
            user_id=user_id
        )

        return transaction

    def create_transaction(self, data: TransactionInScheme, user_id: UUID):  # Need to implement next_due_date rule
        data.user_id = user_id

        self.category_repository.get_category_by_user(
            category_id=data.category_id,
            user_id=user_id
        )

        if data.account_id is not None:
            self.account_repository.get_account_by_user(
                account_id=data.account_id,
                user_id=user_id
            )

        transaction = self.transactions_repository.create(data=data)
        return transaction

    def update_transaction(self, id: UUID, data: TransactionUpdateInScheme, user_id: UUID):
        data.user_id = user_id

        transaction_validated = self.transactions_repository.get_transaction_by_user(
            transaction_id=id,
            user_id=user_id
        )

        if data.category_id is not None:
            self.category_repository.get_category_by_user(
                category_id=data.category_id,
                user_id=user_id
            )
        update_data = data.copy(update={"recurrence_interval": None, "next_due_date": None}) \
            if (data.is_recurring is False and transaction_validated.is_recurring is True) else data

        transaction = self.transactions_repository.update(obj_id=transaction_validated.id, data=update_data)

        return transaction

    def delete_transaction(self, id: UUID, user_id: UUID):
        transaction_validated = self.transactions_repository.get_transaction_by_user(
            transaction_id=id,
            user_id=user_id)
        transaction = self.transactions_repository.soft_delete(obj_id=transaction_validated.id)
        return transaction

    def restore_transaction(self, id: UUID, user_id: UUID):
        deleted_transaction = self.transactions_repository.get_deleted_transaction_by_user(
            transaction_id=id,
            user_id=user_id
        )
        transaction = self.transactions_repository.restore(obj_id=deleted_transaction.id)
        return transaction

    def force_delete_transaction(self, id: UUID, user_id: UUID):
        deleted_transaction = self.transactions_repository.get_deleted_transaction_by_user(
            transaction_id=id,
            user_id=user_id
        )
        transaction = self.transactions_repository.force_delete(obj_id=deleted_transaction.id)
        return transaction