from datetime import datetime

from sqlalchemy.orm import Session

from transactions.models import Transactions as TransactionModel, RecurrenceSchedule as RecurrenceScheduleModel
from transactions.utils import _calculate_next_date


def process_recurring_transactions(db: Session):
    now = datetime.now()

    # 1. Search shedules that needs to be executad today
    recurring_schedules_to_process = db.query(RecurrenceScheduleModel).filter(
        RecurrenceScheduleModel.is_active == True,
        RecurrenceScheduleModel.next_due_date <= now,
        RecurrenceScheduleModel.deleted_at == None
    ).all()

    for recurring_schedule in recurring_schedules_to_process:
        # 2. Search for the "Mother Transaction" to copy their data (or the last one generated)
        mother_transaction = db.query(TransactionModel).filter(
            TransactionModel.recurrence_id == recurring_schedule.id
        ).order_by(TransactionModel.date.desc()).first()

        if mother_transaction:
            # 3. Creates a NEW transaction for the current month
            new_transaction = TransactionModel(
                user_id=recurring_schedule.user_id,
                account_id=mother_transaction.account_id,
                category_id=mother_transaction.category_id,
                recurrence_id=recurring_schedule.id,
                name=mother_transaction.name,
                description=mother_transaction.description,
                amount=mother_transaction.amount,
                date=recurring_schedule.next_due_date,
            )
            db.add(new_transaction)

            # 4. Calculates the next due date
            recurring_schedule.next_due_date = _calculate_next_date(
                start_date=recurring_schedule.next_due_date,
                interval=recurring_schedule.interval
            )

            # 5. Verifies if reached end date
            if recurring_schedule.end_date and recurring_schedule.next_due_date > recurring_schedule.end_date:
                recurring_schedule.is_active = False

    db.commit()