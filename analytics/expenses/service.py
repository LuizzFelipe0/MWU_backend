from collections import defaultdict
from typing import Optional
from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import Session

from categories.service import CategoryService
from transactions.models import Transactions as TransactionsModel
from mwu.db import get_db
from mwu.repositories.operational_repositories import ModelOperationalRepository, ModelRelationRepository
from transactions.service import TransactionsService
from user.service import UserService
from user_account.models import UsersAccounts as UserAccountModel


class ExpensesService(ModelOperationalRepository):
    def __init__(self, session: Session = Depends(get_db)):
        super().__init__(model=TransactionsModel, session=session)
        self.transaction_service = TransactionsService(session=session)
        self.category_service = CategoryService(session=session)
        self.user_service = UserService(session=session)
        self.relation_repository = ModelRelationRepository(
            relation_model=UserAccountModel,
            first_model_key="user_id",
            second_model_key="account_id",
            session=session
        )

    def get_monthly_expenses_by_category(self, user_id: UUID, is_recurring_expense: Optional[bool] = None):
        transactions_data = self.transaction_service.get_transactions_with_category_type_info(
            user_id, is_recurring_expense
        )

        summary = defaultdict(float)
        totals_by_month = defaultdict(float)

        for item in transactions_data:
            if not item['date']:
                continue

            key = (
                item['date'].year,
                item['date'].month,
                item['category_type_name'],
                item['is_positive'],
            )
            summary[key] += item['amount']
            totals_by_month[(item['date'].year, item['date'].month)] += item['amount']

        result = []
        for (year, month, category_type_name, is_positive), total_amount in summary.items():
            month_total = totals_by_month[(year, month)]
            percentage = round((total_amount / month_total) * 100, 2) if month_total > 0 else 0

            result.append({
                "year": year,
                "month": month,
                "category_type_name": category_type_name,
                "is_positive": is_positive,
                "percentage": percentage,
                "total_amount": round(total_amount, 2)
            })

        return sorted(result, key=lambda x: (x['year'], x['month']))

    def get_total_expense_distribution(self, user_id: UUID):
        transactions_data = self.transaction_service.get_transactions_with_category_type_info(user_id)

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

