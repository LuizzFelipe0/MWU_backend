from datetime import datetime
from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import Session

from accounts.repository import AccountRepository
from categories.repository import CategoryRepository
from category_types.repository import CategoryTypeRepository
from mwu.db import get_db

from .repository import TransactionsRepository, RecurrenceScheduleRepository
from .schemas import TransactionInput as TransactionInScheme, TransactionUpdateInput as TransactionUpdateInScheme
from .utils import _calculate_next_date


class TransactionsService:
    def __init__(self, session: Session = Depends(get_db)):
        self.transactions_repository = TransactionsRepository(session)
        self.recurrence_schedule_repository = RecurrenceScheduleRepository(session)
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

    def create_transaction(self, data: TransactionInScheme, user_id: UUID):
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

        transaction_dict = data.model_dump(exclude={'is_recurring', 'recurrence_interval', 'end_date', 'next_due_date'})
        transaction_dict["user_id"] = user_id

        recurrence_schedule_dict = None
        if data.is_recurring:

            next_date = data.next_due_date
            if not next_date:
                next_date = _calculate_next_date(start_date=data.date, interval=data.recurrence_interval)

            recurrence_schedule_dict = {
                "user_id": user_id,
                "interval": data.recurrence_interval,
                "next_due_date": next_date,
                "end_date": None,
                "is_active": True
            }

        transaction = self.transactions_repository.create_transaction_with_recurrence(transaction_dict, recurrence_schedule_dict)
        return transaction

    def update_transaction(self, id: UUID, data: TransactionUpdateInScheme, user_id: UUID):
        data.user_id = user_id
        self.transactions_repository.get_transaction_by_user(id, user_id)

        if data.category_id:
            self.category_repository.get_category_by_user(data.category_id, user_id)

        transaction_fields = data.model_dump(exclude_unset=True, exclude={
            'is_recurring', 'recurrence_interval', 'end_date', 'next_due_date'
        })

        schedule_fields = None
        stop_recurrence = False

        if data.is_recurring is False:
            stop_recurrence = True

        elif data.is_recurring is True:
            interval = data.recurrence_interval or "MONTHLY"

            next_date = data.next_due_date
            if not next_date:
                next_date = _calculate_next_date(start_date=datetime.now(), interval=interval)

            schedule_fields = {
                "user_id": user_id,
                "interval": interval,
                "next_due_date": next_date,
                "end_date": data.end_date,
                "is_active": True,
                "updated_at": datetime.now()
            }
            schedule_fields = {k: v for k, v in schedule_fields.items() if v is not None}

        transaction = self.transactions_repository.update_transaction_with_recurrence(
            transaction_id=id,
            transaction_data=transaction_fields,
            schedule_data=schedule_fields,
            stop_recurrence=stop_recurrence
        )

        return transaction

    def delete_transaction(self, id: UUID, user_id: UUID):
        transaction_validated = self.transactions_repository.get_transaction_by_user(
            transaction_id=id,
            user_id=user_id)

        transaction = self.transactions_repository.soft_delete_with_cascade_on_recurrences(transaction_id=transaction_validated.id)

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