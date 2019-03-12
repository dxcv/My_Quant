# encoding=utf-8
from apscheduler.schedulers.blocking import BlockingScheduler

def trigger():
    print(str)

sched = BlockingScheduler()
sched.add_job(trigger, 'cron', day_of_week='mon-fri', hour='9-12, 13-15', minute='*/5')

sched.start()