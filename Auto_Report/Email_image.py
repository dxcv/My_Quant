# encoding = utf-8
import smtplib
import traceback
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import tushare as ts
from General.GlobalSetting import *
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
# !/usr/bin/python
# coding:utf-8


import smtplib
import mimetypes
# from email import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

# fromaddr = "ai_report@163.com"
fromaddr = "pwnevy@163.com"
smtpaddr = "smtp.163.com"

toaddrs = ["1210055099@qq.com"]
subject = "AI自动报告-V1"
# password = "ypw1989"
password = "87315287"


#!/usr/bin/env python3
#coding: utf-8
import smtplib
from email.mime.text import MIMEText

sender = fromaddr
receiver = toaddrs
subject = '本日报告'
smtpserver = 'smtp.163.com'
username = fromaddr
password = password

msg = MIMEText('下午开会')

msg['Subject'] = subject

smtp = smtplib.SMTP()
smtp.connect('smtp.163.com')
smtp.login(username, password)
smtp.sendmail(sender, receiver, msg.as_string())
smtp.quit()
