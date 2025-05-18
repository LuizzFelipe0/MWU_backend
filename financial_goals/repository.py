from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import Session

from mwu.db import get_db
from mwu.services.operational_services import ModelOperationalService
from user.models import User as UserModel
from .models import FinancialGoals as FinancialGoalsModel
from .schemas import FinancialGoalsInput as FinancialGoalsInScheme, \
    FinancialGoalsUpdateInput as FinancialGoalsUpdateInScheme


class FinancialGoalsRepository(ModelOperationalService):
    def __init__(self, session: Session = Depends(get_db)):
        super().__init__(model=FinancialGoalsModel, session=session)
        self.user_service = ModelOperationalService(UserModel, session=session)

    def get_all_financial_goals(self):
        financial_goals = self.get_all()
        return financial_goals

    def get_financial_goal_by_id(self, id: UUID):
        financial_goal = self.get_obj_by_id(obj_id=id)
        return financial_goal

    def create_financial_goal(self, data: FinancialGoalsInScheme):
        self.user_service.get_obj_by_id_not_deleted(data.user_id)

        financial_goal = self.create(data=data)
        return financial_goal

    def update_financial_goal(self, id: UUID, data: FinancialGoalsUpdateInScheme):
        financial_goal_with_id_validated = self.get_obj_by_id(id)

        if data.user_id is not None:
            self.get_obj_by_id_not_deleted(data.user_id)

        financial_goal = self.update(obj_id=financial_goal_with_id_validated.id, data=data)
        return financial_goal

    def delete_financial_goal(self, id: UUID):
        financial_goal_with_id_validated = self.get_obj_by_id(id)
        financial_goal = self.force_delete(obj_id=financial_goal_with_id_validated.id)
        return financial_goal
