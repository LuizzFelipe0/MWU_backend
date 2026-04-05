from collections import defaultdict
from typing import Optional
from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import Session

from categories.repository import CategoryRepository
from category_types.repository import CategoryTypeRepository
from mwu.db import get_db
from transactions.repository import TransactionsRepository
from user.repository import UserRepository


class ExpensesService:
    def __init__(self, session: Session = Depends(get_db)):
        self.transaction_service = TransactionsRepository(session=session)
        self.category_service = CategoryRepository(session=session)
        self.category_type_service = CategoryTypeRepository(session=session)
        self.user_service = UserRepository(session=session)


    def get_transactions(self, user_id: UUID, is_recurring_expense: Optional[bool] = None):
            transactions = self.transaction_service.get_transactions_by_user(user_id=user_id)

            if is_recurring_expense is not None:
                transactions = [t for t in transactions if t.is_recurring == is_recurring_expense]

            result = []
            for transaction in transactions:
                category = self.category_service.get_category_by_user(category_id=transaction.category_id, user_id=user_id)
                category_type = self.category_type_service.get_by_id(obj_id=category.category_type_id)

                result.append({
                    "amount": transaction.amount,
                    "date": transaction.date,
                    "category_name": category.name,
                    "category_type_name": category_type.name,
                    "is_positive": category_type.is_positive
                })
            return result


    def get_monthly_expenses(self, user_id: UUID, is_recurring_expense: Optional[bool] = None):
        transactions_data = self.get_transactions(user_id=user_id, is_recurring_expense=is_recurring_expense)

        summary = defaultdict(float)
        totals_by_month = defaultdict(float)

        for item in transactions_data:
            if not item['date']:
                continue

            key = (
                item['date'].year,
                item['date'].month,
                item['category_type_name'],
                item['category_name'],
                item['is_positive'],
            )
            summary[key] += item['amount']
            totals_by_month[(item['date'].year, item['date'].month)] += item['amount']

        result = []
        for (year, month, category_type_name, category_name, is_positive), total_amount in summary.items():
            month_total = totals_by_month[(year, month)]
            percentage = round((total_amount / month_total) * 100, 2) if month_total > 0 else 0

            result.append({
                "year": year,
                "month": month,
                "category_type_name": category_type_name,
                "category_name": category_name,
                "is_positive": is_positive,
                "percentage": percentage,
                "total_amount": round(total_amount, 2)
            })

        return sorted(result, key=lambda x: (x['year'], x['month']))

    def get_total_expense_distribution(self, user_id: UUID):
        transactions_data = self.get_transactions(user_id=user_id)

        valid_transactions = [t for t in transactions_data if t.get('date')]
        total = sum(t['amount'] for t in valid_transactions)

        if total == 0:
            return []

        category_totals = defaultdict(float)
        for t in valid_transactions:
            category_totals[t['category_type_name']] += t['amount']

        return [
            {
                "category_type_name": category_type_name,
                "percentage": round((amount / total) * 100, 2)
            }
            for category_type_name, amount in category_totals.items()
        ]
