# encoding = utf-8
from General.GlobalSetting import *

# 与时间相关的自定义函数文件



# 将“2017.8”转成“2017.08”，否则在画图时会出现错乱，因为画图时8会大于12
def stdMonthDate(month_str):

    str_split = month_str.split('.')
    if int(str_split[1]) <10:
        str_split[1] = "0"+str_split[1]

    return str_split[0]+'.'+str_split[1]
