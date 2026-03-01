from datetime import date
from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import Session

from accounts.service import AccountService
from financial_goals.service import FinancialGoalsService
from mwu.db import get_db
from user.service import UserService


class GoalsService:
    def __init__(self, session: Session = Depends(get_db)):
        self.financial_goals_service = FinancialGoalsService(session=session)
        self.account_service = AccountService(session=session)
        self.user_service = UserService(session=session)

    def get_goals_to_be_reached(self, user_id: UUID):
        global monthly_saving_required
        
        accounts = self.account_service.get_all_accounts(user_id=user_id)
        financial_goals = self.financial_goals_service.get_all_financial_goals(user_id=user_id)
        user = self.user_service.get_user_by_id(id=user_id)

        sum_of_account_balances = sum(acc.balance for acc in accounts)
        user_manual_balance = user.manual_balance or 0

        sum_of_balances = sum_of_account_balances + user_manual_balance

        today = date.today()
        goals_progress = []
        for goal in financial_goals:
            difference_to_achieve_target = max(0, round(goal.target_amount - sum_of_balances,8))

            progress_percentage = f"{round(min(100, (sum_of_balances / goal.target_amount) * 100))}%"

            if goal.deadline and goal.deadline > today and difference_to_achieve_target > 0:
                months_remaining = ((goal.deadline.year - today.year) * 12 + goal.deadline.month - today.month)
                if goal.deadline.day < today.day:
                    months_remaining -= 1
                months_remaining = max(months_remaining, 1)
                monthly_saving_required = round(difference_to_achieve_target / months_remaining, 2)

            goals_progress.append({
                "id": goal.id,
                "name": goal.name,
                "description": goal.description,
                "target_amount": goal.target_amount,
                "progress_percentage": progress_percentage,
                "difference_to_achieve_target": difference_to_achieve_target,
                "sum_of_balances": sum_of_balances,
                "deadline": goal.deadline,
                "monthly_saving_required": monthly_saving_required,
            })
        return goals_progress
