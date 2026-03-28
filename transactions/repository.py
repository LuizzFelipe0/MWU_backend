from datetime import datetime
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import extract
from sqlalchemy.orm import Session
from mwu.repositories.base_repository import BaseRepository
from .models import Transactions as TransactionModel, RecurrenceSchedule as RecurrenceScheduleModel

class TransactionsRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session=session, model=TransactionModel)

    def _get_transaction_scoped_query(self, user_id: UUID, is_deleted: bool = False):
        return self._get_query().filter(
            self.model.user_id == user_id,
            self.model.deleted_at.isnot(None) if is_deleted else self.model.deleted_at.is_(None)
        )

    def get_transactions_by_user(self, user_id: UUID, year: int = None, month: int = None):
        transactions = self._get_transaction_scoped_query(user_id)

        if year:
            transactions = transactions.filter(extract('year', self.model.date) == year)
        if month:
            transactions = transactions.filter(extract('month', self.model.date) == month)

        return transactions.all()

    def get_deleted_transactions_by_user(self, user_id: UUID):
        return self._get_transaction_scoped_query(user_id, is_deleted=True).all()

    def get_transaction_by_user(self, transaction_id: UUID, user_id: UUID):
        transaction = self._get_transaction_scoped_query(user_id).filter(self.model.id == transaction_id).first()

        if not transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")
        return transaction
    
    def get_deleted_transaction_by_user(self, transaction_id: UUID, user_id: UUID):
        transaction = self._get_transaction_scoped_query(user_id, is_deleted=True).filter(
            self.model.id == transaction_id).first()
        if not transaction:
            raise HTTPException(status_code=404, detail="Deleted transaction not found")
        return

    def create_transaction_with_recurrence(self, transactions_data: list[dict], schedule_data: dict = None):
        recurrence_id = None

        # 1. If the recurrence is true, it first creates the transaction to obtain ID
        if schedule_data:
            new_schedule = RecurrenceScheduleModel(**schedule_data)
            self.db.add(new_schedule)
            self.db.flush()
            recurrence_id = new_schedule.id

        # 2. Inserts all transactions (being 1 or more in the past)
        created_transactions = []
        for transaction_dict in transactions_data:
            transaction_dict["recurrence_id"] = recurrence_id
            new_tr = self.model(**transaction_dict)
            self.db.add(new_tr)
            created_transactions.append(new_tr)

        self.db.commit()

        for tra in created_transactions:
            self.db.refresh(tra)

        return created_transactions[-1]

    def update_transaction_with_recurrence(self, transaction_id: UUID, transaction_data: dict,
                                           schedule_data: dict = None, stop_recurrence: bool = False):
        transaction = self.get_by_id(transaction_id)

        if stop_recurrence and transaction.recurrence_id:
            self.db.query(RecurrenceScheduleModel).filter(
                RecurrenceScheduleModel.id == transaction.recurrence_id
            ).update({"is_active": False, "updated_at": datetime.now()})

        elif schedule_data:
            if transaction.recurrence_id:
                schedule_data["is_active"] = True
                self.db.query(RecurrenceScheduleModel).filter(
                    RecurrenceScheduleModel.id == transaction.recurrence_id
                ).update(schedule_data)
            else:
                new_schedule = RecurrenceScheduleModel(**schedule_data)
                self.db.add(new_schedule)
                self.db.flush()
                transaction.recurrence_id = new_schedule.id

        for key, value in transaction_data.items():
            setattr(transaction, key, value)

        self.db.commit()
        self.db.refresh(transaction)
        return transaction

    def soft_delete_with_cascade_on_recurrences(self, transaction_id: UUID):
        transaction = self.get_by_id(transaction_id)
        now = datetime.now()

        transaction.deleted_at = now

        if transaction.recurrence_id:
            self.db.query(RecurrenceScheduleModel).filter(
                RecurrenceScheduleModel.id == transaction.recurrence_id
            ).update({"deleted_at": now, "is_active": False, "updated_at": now})

        self.db.commit()
        return transaction


class RecurrenceScheduleRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session=session, model=RecurrenceScheduleModel)

