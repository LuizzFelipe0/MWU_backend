import logging
from apscheduler.schedulers.background import BackgroundScheduler
from mwu.db import SessionLocal
from transactions.workers.recurrence_schedule_worker import process_recurring_transactions

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Scheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self._setup_jobs()

    def _setup_jobs(self):
        # Job 1: Process recurring transactions
        self.scheduler.add_job(
            self.recurrence_job_task,
            'cron',
            hour=0,
            minute=1,
            id='recurring_transactions_job',
            replace_existing=True
        )

        logger.info("Scheduler: All jobs has been configured.")

    def recurrence_job_task(self):
        logger.info("Scheduler: Initialzed process_recurring_transactions...")
        db = SessionLocal()
        try:
            count = process_recurring_transactions(db)
            logger.info(f"Scheduler: Finish job. {count} transactions generated.")
        except Exception as e:
            logger.error(f"Scheduler: Error on recurrence_job_task: {e}")
        finally:
            db.close()

    def start(self):
        if not self.scheduler.running:
            self.scheduler.start()
            logger.info("Scheduler: Initialized!")

    def shutdown(self):
        if self.scheduler.running:
            self.scheduler.shutdown()
            logger.info("Scheduler: Disabled!.")


mwu_scheduler = Scheduler()