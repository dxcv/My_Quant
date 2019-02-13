# enconding = utf-8

import time
from apscheduler.schedulers.blocking import BlockingScheduler

from Auto_Report.ReportLab.test1 import send_basic_email
from General.GlobalSetting import conn_k
from LoadHistoryData.Update_K_Data import update_K_data
from Test.MACD_Timer import macd_test_daily


sched = BlockingScheduler()
sched.add_job(func=MACD_Report, trigger='cron', day_of_week='mon-sat', hour=5, minute=0)
sched.add_job(func=update_k, trigger='cron', day_of_week='mon-sat', hour=6, minute=30)
sched.start()