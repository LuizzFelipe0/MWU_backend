from fastapi import APIRouter,Depends
from fastapi_utils.cbv import cbv

from analytics.goals.schemas import GoalsOutput

from analytics.goals.service import GoalsService
from auth.utils import get_current_user

goals_router = APIRouter(prefix="/goals-analysis", tags=["Goals Analysis"])


@cbv(goals_router)
class GoalsController:
    service: GoalsService = Depends()

    @goals_router.get("/all", response_model=list[GoalsOutput])
    def get_all(self, current_user = Depends(get_current_user)):
        goals = self.service.get_goals_to_be_reached(user_id=current_user.id)
        return goals