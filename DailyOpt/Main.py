# encoding=utf-8
import pickle
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.combining import OrTrigger
from apscheduler.triggers.cron import CronTrigger

from CornerDetectAndAutoEmail.AveMaxMinDetect.Global import h_l_pot_info_url, price_ratio_info_url
from CornerDetectAndAutoEmail.AveMaxMinDetect.MaxMin import judgeAndSendMsg, updatePotInfo

import os

from General.AutoStkConfig import stk_list

""" 
打印关心的股票当前价格在历史上是什么位置
"""


if os.path.exists(price_ratio_info_url):
    try:
        with open(price_ratio_info_url, 'rb') as f:
            price_ratio_info = pickle.load(f)

            if len(price_ratio_info) != len(stk_list):
                updatePotInfo()
    except:
        updatePotInfo()
else:
    updatePotInfo()


sched = BlockingScheduler()
trigger = OrTrigger([
    CronTrigger(hour='9', minute='31-59/5'),
    CronTrigger(hour='10', minute='*/5'),
    CronTrigger(hour='11', minute='1-29/5'),
    CronTrigger(hour='13-15', minute='*/5')

])
sched.add_job(judgeAndSendMsg,
              trigger,
              day_of_week='mon-fri',
              minute='*/5',
              max_instances=10)

sched.add_job(func=updatePotInfo, trigger='cron', day_of_week='mon-fri', hour=5, minute=30, misfire_grace_time=3600, coalesce=True)
# sched.add_job(updatePotInfo,
#               'cron',
#               max_instances=10,
#               second='*/35', misfire_grace_time=3600, coalesce=True)

sched.start()
