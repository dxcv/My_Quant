# encoding=utf-8
from apscheduler.executors import tornado
from apscheduler.schedulers.blocking import BlockingScheduler

from CornerDetectAndAutoEmail.AveMaxMinDetect.MaxMin import judgeAndSendMsg, h_l_poy_info, updatePotInfo


def trigger():
    print(str)

sched = BlockingScheduler()

sched.add_job(judgeAndSendMsg,
              'cron',
              day_of_week='mon-fri',
              hour='9-12, 13-23',
              minute='*/2',
              max_instances=10,
              kwargs={"df_H_L_Pot": h_l_poy_info})


sched.add_job(updatePotInfo,
              'cron',
              max_instances=10,
              second='*/35', misfire_grace_time=3600, coalesce=True)

sched.start()
tornado.ioloop.IOLoop.instance().start()