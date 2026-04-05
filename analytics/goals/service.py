from datetime import date
from typing import Any, Dict, Optional
from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import Session

from accounts.repository import AccountRepository
from financial_goals.repository import FinancialGoalsRepository
from mwu.db import get_db
from user.repository import UserRepository


class GoalsService:
    def __init__(self, session: Session = Depends(get_db)):
        self.financial_goals_repository = FinancialGoalsRepository(session=session)
        self.account_repository = AccountRepository(session=session)
        self.user_repository = UserRepository(session=session)

    def _calculate_progress(self, goal: Any, balance: float) -> Dict[str, Any]:
        today = date.today()

        difference = max(0.0, round(goal.target_amount - balance, 2))
        percentage_num = min(100, (balance / goal.target_amount) * 100) if goal.target_amount > 0 else 0
        progress_percentage = f"{round(percentage_num)}%"

        monthly_saving_required = 0.0
        if goal.deadline and goal.deadline > today and difference > 0:
            months_remaining = ((goal.deadline.year - today.year) * 12 + goal.deadline.month - today.month)
            if goal.deadline.day < today.day:
                months_remaining -= 1

            months_remaining = max(months_remaining, 1)
            monthly_saving_required = round(difference / months_remaining, 2)

        return {
            "id": goal.id,
            "name": goal.name,
            "description": goal.description,
            "target_amount": goal.target_amount,
            "progress_percentage": progress_percentage,
            "sum_of_balances": round(balance, 2),
            "difference_to_achieve_target": difference,
            "deadline": goal.deadline,
            "monthly_saving_required": monthly_saving_required,
        }

    def get_goals_to_be_reached(self, user_id: UUID, account_id: Optional[str] = None):
        financial_goals = self.financial_goals_repository.get_financial_goals_by_user(user_id=user_id)

        balance_to_use = 0.0

        if account_id == "total" or not account_id:
            accounts = self.account_repository.get_accounts_by_user(user_id=user_id)
            user = self.user_repository.get_by_id(obj_id=user_id)
            balance_to_use = sum(acc.balance for acc in accounts) + (user.manual_balance or 0)

        elif account_id == "manual":
            user = self.user_repository.get_by_id(obj_id=user_id)
            balance_to_use = user.manual_balance or 0

        else:
            account = self.account_repository.get_account_by_user(account_id=UUID(account_id), user_id=user_id)
            balance_to_use = account.balance

        return [self._calculate_progress(goal, balance_to_use) for goal in financial_goals]