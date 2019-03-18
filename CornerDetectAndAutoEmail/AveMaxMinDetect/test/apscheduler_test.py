# encoding=utf-8
import pickle
from apscheduler.schedulers.blocking import BlockingScheduler

from CornerDetectAndAutoEmail.AveMaxMinDetect.Global import h_l_pot_info_url
from CornerDetectAndAutoEmail.AveMaxMinDetect.MaxMin import judgeAndSendMsg, updatePotInfo


sched = BlockingScheduler()
sched.add_job(judgeAndSendMsg,
              'cron',
              day_of_week='mon-fri',
              hour='9-12, 13-15',
              minute='*/5',
              max_instances=10)

sched.add_job(func=updatePotInfo, trigger='cron', day_of_week='mon-fri', hour=5, minute=30, misfire_grace_time=3600, coalesce=True)
# sched.add_job(updatePotInfo,
#               'cron',
#               max_instances=10,
#               second='*/35', misfire_grace_time=3600, coalesce=True)

sched.start()