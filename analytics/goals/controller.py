from uuid import UUID

from fastapi import APIRouter,Depends
from fastapi_utils.cbv import cbv

from analytics.goals.schemas import GoalsOutput

from analytics.goals.service import GoalsService

analytics_router = APIRouter(prefix="/analytics", tags=["Analytics"])


@cbv(analytics_router)
class GoalsController:
    service: GoalsService = Depends()

    @analytics_router.get("/{user_id}", response_model=list[GoalsOutput])
    def get_goals_to_be_reached_by_user(self, user_id: UUID):
        goals = self.service.get_goals_to_be_reached_by_user(user_id=user_id)
        return goals