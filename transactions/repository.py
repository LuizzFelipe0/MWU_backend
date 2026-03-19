from datetime import datetime
from uuid import UUID

from fastapi import HTTPException
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

    def get_transactions_by_user(self, user_id: UUID):
        return self._get_transaction_scoped_query(user_id).all()

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

    def create_transaction_with_recurrence(self, transaction_data: dict, schedule_data: dict = None):

        if schedule_data:

            new_schedule = RecurrenceScheduleModel(**schedule_data)
            self.db.add(new_schedule)
            self.db.flush()

            transaction_data["recurrence_id"] = new_schedule.id

        new_transaction = self.model(**transaction_data)
        self.db.add(new_transaction)

        self.db.commit()
        self.db.refresh(new_transaction)
        return new_transaction

    def update_transaction_with_recurrence(self, transaction_id: UUID, transaction_data: dict, schedule_data: dict = None,
                                         stop_recurrence: bool = False):
        transaction = self.get_by_id(transaction_id)

        if stop_recurrence and transaction.recurrence_id:

            self.db.query(RecurrenceScheduleModel).filter(
                RecurrenceScheduleModel.id == transaction.recurrence_id
            ).update({"deleted_at": datetime.now(), "is_active": False})

            transaction.recurrence_id = None

        elif schedule_data:
            if transaction.recurrence_id:

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

        transaction.deleted_at = datetime.now()

        if transaction.recurrence_id:
            self.db.query(RecurrenceScheduleModel).filter(
                RecurrenceScheduleModel.id == transaction.recurrence_id
            ).update({"deleted_at": datetime.now(), "is_active": False})

        self.db.commit()
        return transaction


class RecurrenceScheduleRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session=session, model=RecurrenceScheduleModel)

