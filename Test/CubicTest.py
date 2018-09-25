# encoding = utf-8

from General.GlobalSetting import *
from SDK.SDKHeader import *
import talib
"""
    三次样条拟合测试
"""


import matplotlib.pyplot as plt
import numpy as np

sh_index = ts.get_hist_data('cyb')
sh_index['date'] = sh_index.index


# 按时间降序排序，方便计算macd
sh_index = sh_index.sort_values(by='date', ascending=True)

# 在原始df中增加macd信息
sh_index['MACD'], sh_index['MACDsignal'], sh_index['MACDhist'] = talib.MACD(sh_index.close,
                                                                            fastperiod=12, slowperiod=26,
                                                                            signalperiod=9)

sh_index = sh_index.dropna(how='any',axis=0).reset_index(drop=True)
for idx in sh_index.loc[6:,:].index:
    df_part = sh_index.loc[idx-5:idx,'MACD'].reset_index(drop=True)

    c=np.polyfit(np.array(df_part.index),np.array(df_part),2)

    a = c[0]
    b = c[1]
    bottom = -1*(b/(2*a))

    if 4 < bottom < 6:
        plt.plot(df_part)
