# encoding=utf-8

"""
本脚本用于定时提示now表中的stk数据
"""
from General.GlobalSetting import g_total_stk_info_mysql
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
from General.AutoStkConfig import stk_list
import tushare as ts
import win32gui
import win32con
import time
from DesktopWindow.ShowWindowsMsg import TestTaskbarIcon
import math

from SendMsgByGUI.QQGUI import send_qq

""" =========================== 子函数 ============================ """
earn_threshold = 120            # 挣100来块前就满足了
remind_ratio = 0.9              # 操作提前提醒
continuous_seconds = 240        # 提醒信息持续时间

money_each_opt = 5000


def JudgeSingleStk(stk_code, stk_price_last, stk_amount_last):

    # 获取该股票的实时价格
    current_price = float(ts.get_realtime_quotes(stk_code)['price'].values[0])
    price_diff = current_price - stk_price_last

    if current_price == 0.0:
        print(stk_code + 'price==0.0! 返回！')
        return

    buy_amount = math.floor((money_each_opt/current_price)/100)*100


    if (price_diff * stk_amount_last > earn_threshold*remind_ratio) & (price_diff * stk_amount_last < earn_threshold):
        send_qq('影子', "Near! S! "+stk_code + ' Amount:' + str(stk_amount_last) + '\nP_now:' + str(current_price) + '\nP_last:' + str(stk_price_last))

    elif price_diff * stk_amount_last > earn_threshold:
        send_qq('影子', "Reach! S! "+stk_code + ' Amount:' + str(stk_amount_last) + '\nP_now:' + str(current_price) + '\nP_last:' + str(stk_price_last))

    elif (price_diff*buy_amount > -earn_threshold)&(price_diff*buy_amount < -earn_threshold*remind_ratio):
        send_qq('影子', "Near! B! " + stk_code + ' Amount:' + str(buy_amount) + '\nP_now:' + str(current_price) + '\nP_last:' + str(stk_price_last))

    elif price_diff*buy_amount < -earn_threshold:
        send_qq('影子', "Reach! B! " + stk_code + ' Amount:' + str(buy_amount) + '\nP_now:' + str(current_price) + '\nP_last:' + str(stk_price_last))

    else:
        print('未触发任何警戒线！')


def callback():
    (conn_opt, engine_opt) = genDbConn(localDBInfo, db_name)
    df = pd.read_sql(con=conn_opt, sql='select * from now')
    if not df.empty:
        for idx in df.index:
            stk_code = df.loc[idx, 'stk_code']
            price_last = df.loc[idx, 'price']
            amount_last = df.loc[idx, 'amount']

            JudgeSingleStk(
                stk_code=stk_code,
                stk_price_last=price_last,
                stk_amount_last=amount_last)

    print(str(pd.read_sql(con=conn_opt, sql='select * from now')))
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
    CronTrigger(hour='9', minute='31-59/5'),
    CronTrigger(hour='10', minute='*/5'),
    CronTrigger(hour='11', minute='1-29/5'),
    CronTrigger(hour='13-14', minute='*/5')
])

sched.add_job(callback,
              trigger,
              day_of_week='mon-fri',
              minute='*/5',
              max_instances=10)


if __name__ == '__main__':
    sched.start()
