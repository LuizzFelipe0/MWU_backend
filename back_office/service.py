from uuid import UUID
from sqlalchemy.orm import Session
from fastapi import HTTPException

from transactions.models import Transactions as TransactionModel
from transactions.repository import RecurrenceScheduleRepository
from transactions.utils import _calculate_next_date
from mwu.schedulers.scheduler import mwu_scheduler


class BackOfficeService:
    def __init__(self, session: Session):
        self.recurrence_schedule_repository = RecurrenceScheduleRepository(session)
        self.db = session

    def trigger_global_job(self):
        run_scheduler = mwu_scheduler.recurrence_job_task()

        return run_scheduler

    def simulate_recurrence_flow(self, recurrence_id: UUID, iterations: int):

        schedule = self.recurrence_schedule_repository.get_by_id(recurrence_id)
        if not schedule:
            raise HTTPException(status_code=404, detail="Schedule not found")

        generated_transactions = []

        for i in range(iterations):

            last_transaction = self.db.query(TransactionModel).filter(
                TransactionModel.recurrence_id == schedule.id
            ).order_by(TransactionModel.date.desc()).first()

            if not last_transaction:
                break

            # Creates the "future" transaction
            new_tra = TransactionModel(
                user_id=schedule.user_id,
                account_id=last_transaction.account_id,
                category_id=last_transaction.category_id,
                recurrence_id=schedule.id,
                name=last_transaction.name,
                description=last_transaction.description,
                amount=last_transaction.amount,
                date=schedule.next_due_date
            )
            self.db.add(new_tra)

            # Advance the schedule date to the NEXT iteration
            schedule.next_due_date = _calculate_next_date(schedule.next_due_date, schedule.interval)

            if schedule.end_date and schedule.next_due_date > schedule.end_date:
                schedule.is_active = False
                self.db.add(new_tra)
                break

            generated_transactions.append(new_tra)

        self.db.commit()
        return len(generated_transactions)