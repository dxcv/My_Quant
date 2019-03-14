# encoding=utf-8
import pickle
from apscheduler.schedulers.blocking import BlockingScheduler

from CornerDetectAndAutoEmail.AveMaxMinDetect.Global import h_l_pot_info_url
from CornerDetectAndAutoEmail.AveMaxMinDetect.MaxMin import judgeAndSendMsg, updatePotInfo

import os

from General.AutoStkConfig import stk_list

""" 
每次启动之时，应该检查高低线信息是否存在及是否合适，
存在与否以文件是否存在为准则，合适与否以concerned 的stk数量是否符合为准则（防止新增加stk的情况）
"""
if os.path.exists(h_l_pot_info_url):
    try:
        with open(h_l_pot_info_url, 'rb') as f:
            h_l_pot_info = pickle.load(f)

            if len(h_l_pot_info) != len(stk_list):
                updatePotInfo()
    except:
        updatePotInfo()
else:
    updatePotInfo()


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
