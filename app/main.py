from apscheduler.schedulers.blocking import BlockingScheduler
from app.collector import collect
from logger import logger

scheduler = BlockingScheduler()

scheduler.add_job(
    collect,
    trigger='cron',
    hour='*/6',
    max_instances=1,
    misfire_grace_time=3600
)

if __name__ == "__main__":
    logger.info("Scheduler started")
    scheduler.start()