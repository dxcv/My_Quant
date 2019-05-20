# encoding=utf-8

"""
本脚本通过根据布林线动态调整网格大小

"""


import tushare as ts
import talib
from pylab import *

from Constraint.Constraint import calBSReseau
from SDK.MyTimeOPT import minus_date_str
from SDK.StkSub import BS_opt, plotOPResult

stk_code = '300183'

df = ts.get_k_data(stk_code, start='2017-01-12', end='2019-05-26')


closed = df['close'].values
df['upper'], df['middle'], df['lower'] = talib.BBANDS(closed, timeperiod=10,
                                                        # number of non-biased standard deviations from the mean
                                                        nbdevup=2,
                                                        nbdevdn=2,
                                                        # Moving average type: simple moving average here
                                                        matype=0)

df = df.dropna(how='any', axis=0)
end = 0
"""
画图语句
df.plot('date', ['upper', 'lower', 'high', 'low'], style=['-^', '-^', '*', '*'])

"""