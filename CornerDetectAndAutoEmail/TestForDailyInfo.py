# encoding=utf-8

"""
本脚本用于定时将大盘以及关心的股票的走势情况发送到邮箱，每天一次！

"""
import matplotlib

from General.GlobalSetting import g_total_stk_info_mysql
from SDK.StkSub import getNameByStkCode

matplotlib.use('Agg')
from CornerDetectAndAutoEmail.Email_Sub import sendmailForStk, sendmail
from CornerDetectAndAutoEmail.HtmlStr import *
from CornerDetectAndAutoEmail.Sub import genStkPic, genMIMEImageList
from General.AutoStkConfig import stk_list
from SDK.MyTimeOPT import get_current_date_str
import tushare as ts
from apscheduler.schedulers.blocking import BlockingScheduler


def dailyStkInfoEmail():
    """
    定时器每天要执行的函数,发送所关心的基本的stk信息
    :return:
    """

    """ -------------------------- 组织html --------------------------- """

    # 构造html的单位
    H_str = '' + H_Head                     # html字符串
    date_str = get_current_date_str()       # 获取当前日期
    pic_dir_list = []                       # 用以保存用到的图片的路径

    """ 制定html """
    for stk in stk_list:
        stk_df = ts.get_k_data(stk)

        # 生成图片
        pic_dir_stk = genStkPic(stk_df,
                                stk,
                                date_str,
                                pic_save_dir_root,
                                pic_name='stk_A_C_M.png')

        pic_dir_list.append(pic_dir_stk)

        # 构造html
        H_str = H_str + gen_H_Unit(stk_code=stk,
                                   stk_name=getNameByStkCode(g_total_stk_info_mysql, stk),
                                   pic_dir=pic_dir_stk.replace(pic_save_dir_root, ''))

    H_str = H_str + H_tail

    """ ------------------- 生成需要的图片 ----------------------- """
    msgImage_list = genMIMEImageList(pic_dir_list)

    """ -------------------- 邮件发送 ----------------------- """
    sendmail(
        subject='Darling, daily report for you!',
        MIMEText_Input=MIMEText(H_str, 'html', 'utf-8'),
        MIMEImageList=msgImage_list,
        toaddrs=["pwnevy@163.com"],
        fromaddr="ai_report@163.com",
        smtpaddr="smtp.163.com",
        password="sqm654321")

# 函数测试
# dailyStkInfoEmail()

""" ------------------ 启动定时器 --------------------- """
sched = BlockingScheduler()
# sched.add_job(func=dailyStkInfoEmail, trigger='cron', day_of_week='mon-sat', hour=5, minute=0)
sched.add_job(func=dailyStkInfoEmail, trigger='interval', minutes=5)
sched.start()