# enconding = utf-8

import time
from apscheduler.schedulers.blocking import BlockingScheduler

from General.GlobalSetting import conn_k
from LoadHistoryData.Update_K_Data import update_K_data
from Test.MACD_Timer import macd_test_daily


def MACD_Report():
    macd_test_daily()

def update_k():
    update_K_data()
    conn_k.commit()


sched = BlockingScheduler()
sched.add_job(func=MACD_Report, trigger='cron', day_of_week='mon-sat', hour=5, minute=30)
sched.add_job(func=update_k, trigger='cron', day_of_week='mon-sat', hour=6, minute=30)
sched.start()