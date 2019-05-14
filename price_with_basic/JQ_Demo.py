# encoding=utf-8
from JQData_Test.auth_info import *
import pandas as pd

from SDK.MyTimeOPT import convert_str_to_date

"""
使用JQ数据进行研究
"""


# 查询300183的市值数据
q = query(valuation.pe_ratio,
              valuation.pb_ratio,
              indicator.eps
            ).filter(valuation.code.in_(['300183.XSHE']))

panel = get_fundamentals_continuously(q, end_date='2019-05-12', count=1200)
df_basic = panel.minor_xs('300183.XSHE')
df_basic['date_str'] = df_basic.index
df_basic['date'] = df_basic.apply(lambda x: convert_str_to_date(x['date_str']), axis=1)
df_basic = df_basic.set_index('date')

# 查询收盘价
df_close = get_price(normalize_code('300183'), start_date='2017-01-01', end_date='2019-05-12', frequency='daily', fields=None, skip_paused=False, fq='pre')
df_close = df_close.reset_index()
df_close['date'] = df_close.apply(lambda x: convert_str_to_date(str(x['index'])[:10]), axis=1)
df_close = df_close.set_index('date')

df_concat = pd.concat([df_basic, df_close], axis=1)\
                    .dropna(axis=0)\
                    .loc[:, ['close', 'eps', 'pb_ratio', 'pe_ratio']]


df_concat['date'] = df_concat.index
