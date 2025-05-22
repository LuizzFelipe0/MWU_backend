from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv

from .service import FinancialGoalsService
from .schemas import FinancialGoalsOutput as FinancialGoalOutScheme, FinancialGoalsInput as FinancialGoalInScheme, \
    FinancialGoalsUpdateInput as FinancialGoalUpdateInScheme

financial_goals_router = APIRouter(prefix="/financial_goals", tags=["Financial Goals"])


@cbv(financial_goals_router)
class FinancialGoalsController:
    service: FinancialGoalsService = Depends()

    @financial_goals_router.get("/all", response_model=list[FinancialGoalOutScheme | None])
    def get_all_financial_goals(self):
        financial_goals = self.service.get_all_financial_goals()
        return financial_goals

    @financial_goals_router.get("/{financial_goal_id}", response_model=FinancialGoalOutScheme | None)
    def get_financial_goal_by_id(self, financial_goal_id: UUID):
        financial_goal = self.service.get_financial_goal_by_id(id=financial_goal_id)
        return financial_goal

    @financial_goals_router.post("/create", response_model=FinancialGoalOutScheme, status_code=201)
    def create_financial_goal(self, data: FinancialGoalInScheme) -> FinancialGoalOutScheme:
        financial_goal = self.service.create_financial_goal(data)
        return financial_goal

    @financial_goals_router.patch("/{financial_goal_id}/update", status_code=200)
    def update_financial_goal(self, financial_goal_id: UUID,
                              data: FinancialGoalUpdateInScheme) -> FinancialGoalOutScheme:
        financial_goal = self.service.update_financial_goal(id=financial_goal_id, data=data)
        return financial_goal

    @financial_goals_router.delete("/{financial_goal_id}/delete", status_code=204)
    def delete_financial_goal(self, financial_goal_id: UUID):
        financial_goal = self.service.delete_financial_goal(id=financial_goal_id)
        return financial_goal
