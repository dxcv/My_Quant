# encoding=utf-8

"""
本脚本用于定时将大盘以及关心的股票的走势情况发送到邮箱，每天一次！

"""
from CornerDetectAndAutoEmail.Email_Sub import sendmailForStk
from CornerDetectAndAutoEmail.HtmlStr import *
from CornerDetectAndAutoEmail.Sub import genStkPic
from General.AutoStkConfig import stk_list
from SDK.MyTimeOPT import get_current_date_str
import tushare as ts

""" -------------------------- 组织html --------------------------- """

# 构造html的单位
H_str = '' + H_Head
date_str = get_current_date_str()

for stk in stk_list:
    stk_df = ts.get_k_data(stk)
    pic_dir_stk = genStkPic(stk_df,
                            stk,
                            date_str,
                            pic_save_dir_root,
                            pic_name='stk_A_C_M.png')

    H_str = H_str + gen_H_Unit(stk_code=stk,
                               stk_name=stk,
                               pic_dir=pic_dir_stk)

H_str = H_str + H_tail


# 发送邮件
sendmailForStk(
    fromaddr="ai_report@163.com",
    smtpaddr="smtp.163.com",
    toaddrs=["189916591@qq.com"],
    subject="AI自动报告-V1",
    password="sqm654321",
    html_str=H_str,
    date_str=date_str,
    corner_pot_list=list(result_df_corner['stk_code'])
)