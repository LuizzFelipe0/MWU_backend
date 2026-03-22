from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session
from mwu.db import get_db
from auth.utils import get_current_admin_user
from .service import BackOfficeService
from .schemas import RecurrenceSimulationInput

back_office_router = APIRouter(prefix="/back-office", tags=["Back Office"])

@cbv(back_office_router)
class BackOfficeController:
    session: Session = Depends(get_db)

    @back_office_router.post("/recurrence-schedule-job/run")
    def run_recurrence_schedule_job(self, admin=Depends(get_current_admin_user)):
        service = BackOfficeService(self.session)
        service.trigger_global_job()
        return {"message": "Recurrence schedule job ran successfully!"}

    @back_office_router.post("/recurring-transactions/create")
    def create_future_recurring_transactions(self, data: RecurrenceSimulationInput, admin=Depends(get_current_admin_user)):
        service = BackOfficeService(self.session)
        count = service.simulate_recurrence_flow(data.recurrence_id, data.iterations)
        return {"message": "The Recurring Transactions were created!", "transactions_generated": count}