from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session
from mwu.repositories.base_repository import BaseRepository
from .models import FinancialGoals as FinancialGoalsModel

class FinancialGoalsRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session=session, model=FinancialGoalsModel)

    def _get_financial_goal_scoped_query(self, user_id: UUID):
        return self._get_query().filter(
            self.model.user_id == user_id
        )

    def get_financial_goals_by_user(self, user_id: UUID):
        return self._get_financial_goal_scoped_query(user_id=user_id).all()


    def get_financial_goal_by_user(self, financial_goal_id: UUID, user_id: UUID):
        financial_goal = self._get_financial_goal_scoped_query(user_id=user_id).filter(self.model.id == financial_goal_id).first()
        if not financial_goal:
            raise HTTPException(status_code=404, detail="Financial Goal not found")
        return financial_goal


