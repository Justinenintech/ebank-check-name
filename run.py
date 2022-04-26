# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import threading
from datetime import datetime

from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.executors.pool import ProcessPoolExecutor

from src.app.mb import Tasks
import asyncio


def asyncio_schedule():
    """
    python version >= 3.4.0
    :return:
    """

    t = Tasks()

    executors = {
        'default': ThreadPoolExecutor(20),
        'processpool': ProcessPoolExecutor(5)
    }
    job_defaults = {
        'coalesce': False,
        'max_instances': 5
    }
    scheduler = AsyncIOScheduler(job_defaults=job_defaults, executorsexecutors=executors,
                                 timezone='Asia/Shanghai')
    captcha = input("请输入验证码：")
    scheduler.add_job(t.login, 'date', run_date=datetime.now(), args=[captcha])
    scheduler.add_job(t.get_balance, 'interval', executor='default', seconds=30)
    scheduler.add_job(t.run, 'interval', executor='default', seconds=1)
    scheduler.add_job(t.del_done_task, 'cron', day_of_week='*', hour='1', minute='30', second='30')
    # scheduler.add_job(t.del_done_task,'date', run_date=datetime.now())
    try:
        scheduler.start()
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    asyncio_schedule()
