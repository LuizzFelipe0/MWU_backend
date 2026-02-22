from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import Session

from mwu.db import get_db

from .repository import FinancialGoalsRepository
from .schemas import FinancialGoalsInput as FinancialGoalsInScheme, \
    FinancialGoalsUpdateInput as FinancialGoalsUpdateInScheme


class FinancialGoalsService:
    def __init__(self, session: Session = Depends(get_db)):
        self.financial_goal_repository = FinancialGoalsRepository(session=session)

    def get_all_financial_goals(self, user_id: UUID):
        financial_goals = self.financial_goal_repository.get_financial_goals_by_user(user_id=user_id)
        return financial_goals

    def get_financial_goal_by_id(self, id: UUID, user_id: UUID):
        financial_goal = self.financial_goal_repository.get_financial_goal_by_user(
            financial_goal_id=id,
            user_id=user_id
        )

        return financial_goal

    def create_financial_goal(self, data: FinancialGoalsInScheme, user_id: UUID):
        data.user_id = user_id

        financial_goal = self.financial_goal_repository.create(data=data)
        return financial_goal

    def update_financial_goal(self, id: UUID, data: FinancialGoalsUpdateInScheme, user_id: UUID):
        self.financial_goal_repository.get_financial_goal_by_user(
            financial_goal_id=id,
            user_id=user_id
        )
        data.user_id = user_id

        financial_goal = self.financial_goal_repository.update(obj_id=id, data=data)
        return financial_goal

    def delete_financial_goal(self, id: UUID, user_id: UUID):
        financial_goal_with_id_validated = self.financial_goal_repository.get_financial_goal_by_user(
            financial_goal_id=id,
            user_id=user_id
        )

        financial_goal = self.financial_goal_repository.force_delete(obj_id=financial_goal_with_id_validated.id)
        return financial_goal
