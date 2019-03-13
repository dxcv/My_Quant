# encoding=utf-8
from apscheduler.schedulers.blocking import BlockingScheduler

from CornerDetectAndAutoEmail.AveMaxMinDetect.MaxMin import judgeAndSendMsg, h_l_poy_info, updatePotInfo


sched = BlockingScheduler()

sched.add_job(lambda: judgeAndSendMsg(h_l_poy_info),
              'cron',
              day_of_week='mon-fri',
              hour='9-12, 13-23',
              minute='*/2',
              max_instances=10)


sched.add_job(updatePotInfo,
              'cron',
              max_instances=10,
              second='*/35', misfire_grace_time=3600, coalesce=True)

sched.start()
