import logging
import datetime 
from typing import List 

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from app.core.services import user_service
from app.core.uow.uow import SqlAlchemyUnitOfWork
from app.schemas import user as userSchemas


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SchedulerService:
    async def desable_user_account(self):
        logger.info("I am checking and desabling all accounts that are set")
        run_now = datetime.date.today()

        users_to_disable: List[userSchemas.User] = user_service.get_all_users_to_disable(run_now, uow=SqlAlchemyUnitOfWork())
        print('all users', users_to_disable)
        for user in users_to_disable:
            user_service.update_user(user.id, user_info={'is_active': False}, uow=SqlAlchemyUnitOfWork())
        logger.info("All accounts scheduled to disabled is done!")



    def start(self):
        logger.info("Starting scheduler service.")
        self.sch = AsyncIOScheduler()
        self.sch.start()
        self.sch.add_job(
            self.desable_user_account,
            trigger=CronTrigger(
                day="*", hour="00", minute="00"
            ),
            max_instances=1
        )
    def stop(self):
        logger.info("Ending scheduler service.")
        if self.sch:
            self.sch.shutdown()