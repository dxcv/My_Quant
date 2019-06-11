# encoding=utf-8

"""
本脚本用于定时提示now表中的stk数据
"""
from AutoDailyOpt.AddWeight import calWeight, saveWeightFile
from Auto_Report.Auto_Email.Email_SendPdf import loadPickle
from DailyOpt.TestForDailyInfo import dailyStkInfoEmail
from General.GlobalSetting import g_total_stk_info_mysql
from RelativeRank.Sub import updateConcernStkMData, checkDivergeLowLevel, calRealtimeRank, checkDivergeLowLevel_Sea, \
    updateConcernStkMData_Sea
from SDK.DBOpt import genDbConn
from SDK.MyTimeOPT import get_current_datetime_str
from SDK.StkSub import getNameByStkCode
import pandas as pd
import time
import pickle
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.combining import OrTrigger
from apscheduler.triggers.cron import CronTrigger
from CornerDetectAndAutoEmail.AveMaxMinDetect.Global import h_l_pot_info_url
from CornerDetectAndAutoEmail.AveMaxMinDetect.MaxMin import judgeAndSendMsg, updatePotInfo
import os
from General.AutoStkConfig import stk_list, MDataPWD
import tushare as ts
import win32gui
import win32con
import time
from DesktopWindow.ShowWindowsMsg import TestTaskbarIcon
import math
import numpy as np

from SendMsgByGUI.QQGUI import send_qq

""" =========================== 子函数 ============================ """
basic_earn_threshold = 120      # 100 IS ENOUGH
remind_ratio = 0.8              # 操作提前提醒

basic_ratio = 4               # 获取的每只股票的权值，除以基础ratio，即得到最终加权！

money_each_opt = 5000


def getWeight():

    path = 'D:\My_Quant\AutoDailyOpt\Weight/'

    df = loadPickle(loadLocation=path, fileName='weight')
    if not df.empty:
        return dict(df.loc[:, ['stk_code', 'weight']].to_dict(orient='split')['data'])
    else:
        return {}


def JudgeSingleStk(stk_code, stk_price_last, stk_amount_last, earn_threshold):

    # 获取该股票的实时价格
    current_price = float(ts.get_realtime_quotes(stk_code)['price'].values[0])
    price_diff = current_price - stk_price_last

    if current_price == 0.0:
        print(stk_code + 'price==0.0! 返回！')
        return

    buy_amount = math.floor((money_each_opt/current_price)/100)*100

    # 计算其离心度分数
    try:
        rank9 = calRealtimeRank(
            stk_code=stk_code,
            M_days=9,
            history_data_dir=MDataPWD+'/M_data/')
    except:
        rank9 = -1

    if (price_diff * stk_amount_last > earn_threshold*remind_ratio) & (price_diff * stk_amount_last < earn_threshold):

        send_qq('影子',
                "Near! S! "+stk_code +
                '\nAmount:' + str(stk_amount_last) +
                '\nP_now:' + str(current_price) +
                '\nP_last:' + str(stk_price_last) +
                '\nthreshold:' + str(earn_threshold) +
                '\nM9_rank:' + str('%0.2f' % rank9)
                )

    elif price_diff * stk_amount_last > earn_threshold:
        send_qq('影子',
                "Reach! S! "+stk_code +
                '\nAmount:' + str(stk_amount_last) +
                '\nP_now:' + str(current_price) +
                '\nP_last:' + str(stk_price_last) +
                '\nthreshold:' + str(earn_threshold) +
                '\nM9_rank:' + str('%0.2f' % rank9)
                )

    elif (price_diff*buy_amount > -earn_threshold)&(price_diff*buy_amount < -earn_threshold*remind_ratio):
        send_qq('影子',
                "Near! B! " + stk_code +
                '\nAmount:' + str(buy_amount) +
                '\nP_now:' + str(current_price) +
                '\nP_last:' + str(stk_price_last) +
                '\nthreshold:' + str(earn_threshold) +
                '\nM9_rank:' + str('%0.2f' % rank9)
                )

    elif price_diff*buy_amount < -earn_threshold:
        send_qq('影子',
                "Reach! B! " + stk_code +
                '\nAmount:' + str(buy_amount) +
                '\nP_now:' + str(current_price) +
                '\nP_last:' + str(stk_price_last) +
                '\nthreshold:' + str(earn_threshold) +
                '\nM9_rank:' + str('%0.2f' % rank9))

    else:
        print('未触发任何警戒线！')


def callback():
    (conn_opt, engine_opt) = genDbConn(localDBInfo, db_name)
    df = pd.read_sql(con=conn_opt, sql='select * from now')

    # 获取权值
    weight_dict = getWeight()

    if not df.empty:
        for idx in df.index:
            stk_code = df.loc[idx, 'stk_code']
            price_last = df.loc[idx, 'price']
            amount_last = df.loc[idx, 'amount']

            try:
                if not pd.isnull(weight_dict[stk_code]):
                    earn_threshold = np.max([weight_dict[stk_code]/basic_ratio, 1])*basic_earn_threshold
                else:
                    print(stk_code+':权值为空！使用基础权值！')
                    earn_threshold = basic_earn_threshold
            except:
                print(stk_code+':权值获取失败！使用基础权值！')
                earn_threshold = basic_earn_threshold

            JudgeSingleStk(
                stk_code=stk_code,
                stk_price_last=price_last,
                stk_amount_last=amount_last,
                earn_threshold=int(earn_threshold))

    # print(str(pd.read_sql(con=conn_opt, sql='select * from now')))
    conn_opt.close()


""" =========================== 链接数据库 ============================ """
# 新方式：lacalDBInfo包括除了“数据库名”之外的其他参数
localDBInfo = {'host': 'localhost',
               'port': 3306,
               'user': 'root',
               'password': 'ypw1989',
               'charset': 'utf8'}

db_name = 'stk_opt_info'

table_history = 'history'
table_now = 'now'


""" =========================== 定时器相关 ============================ """
sched = BlockingScheduler()
trigger = OrTrigger([
    CronTrigger(hour='9', minute='31-59/2'),
    CronTrigger(hour='10', minute='*/2'),
    CronTrigger(hour='11', minute='1-29/2'),
    CronTrigger(hour='13-14', minute='*/2')
])

sched.add_job(callback,
              trigger,
              day_of_week='mon-fri',
              minute='*/2',
              max_instances=10)

# 定时筛选离心度高分的stk
sched.add_job(checkDivergeLowLevel,
              trigger,
              day_of_week='mon-fri',
              minute='*/2',
              max_instances=10)

# 定时海选离心度高分的stk
sched.add_job(checkDivergeLowLevel_Sea,
              trigger,
              day_of_week='mon-fri',
              minute='*/5',
              max_instances=10)

sched.add_job(func=dailyStkInfoEmail, trigger='cron', day_of_week='mon-fri', hour=5, minute=0, misfire_grace_time=3600, coalesce=True)
sched.add_job(func=saveWeightFile, trigger='cron', day_of_week='mon-fri', hour=6, minute=0, misfire_grace_time=3600, coalesce=True)


# 更新离心度历史数据
sched.add_job(func=updateConcernStkMData, trigger='cron', day_of_week='mon-fri', hour=5, minute=30, misfire_grace_time=3600, coalesce=True)

# 更新海选离心度历史数据
sched.add_job(func=updateConcernStkMData_Sea, trigger='cron', day_of_week='mon-fri', hour=6, minute=30, misfire_grace_time=3600, coalesce=True)

if __name__ == '__main__':

    sched.start()
