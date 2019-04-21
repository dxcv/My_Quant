# encoding=utf-8

"""
本脚本通过根据布林线动态调整网格大小

"""


import tushare as ts
import talib
from pylab import *

from SDK.StkSub import BS_opt, plotOPResult

stk_code = '300580'

df = ts.get_k_data(stk_code, start='2017-01-12', end='2019-05-26')


closed = df['close'].values
df['upper'], df['middle'], df['lower'] = talib.BBANDS(closed, timeperiod=10,
                                                        # number of non-biased standard deviations from the mean
                                                        nbdevup=2,
                                                        nbdevdn=2,
                                                        # Moving average type: simple moving average here
                                                        matype=0)

df = df.dropna(how='any', axis=0)


record_info = {
    'floor_last': 0,
    'money_remain': 20000,
    'amount_remain': 1500,
    'M_last': -1,                                   # 用以记录上次的均线值，在反向操作中（本次操作与上次不同的情况）使用上次均值！
    'BS_last': 'init',                              # 上次是买还是卖    "buy"   "false"     "init"
    'price_last': df.head(1)['close'].values[0],    # 上次价格
    'BS_trend_now': 'init',
    'BS_real': 'NO_OPT',                            # 本次实际操作
    'Price_now': 12,
    'last_opt_date': '2018-12-15',
    'B_continue': 2,
    'S_continue': 1,
    'B_Reseau': -1,
    'S_Reseau': -1
}

origin_amount = record_info['money_remain']/df.head(1)['close'].values[0] + record_info['amount_remain']


# 遍历df
for idx in df.index:

    df.loc[idx, 'reseau'] = (df.loc[idx, 'upper'] - df.loc[idx, 'middle'])/5
    df.loc[idx, 'now-last'] = df.loc[idx, 'close'] - record_info['price_last']
    now_last = df.loc[idx, 'close'] - record_info['price_last']

    # 确定网格
    reseau = np.max([(df.loc[idx, 'upper'] - df.loc[idx, 'middle'])/8, 0.5])

    # 向上运行，触发S操作
    if df.loc[idx, 'close'] - record_info['price_last'] > reseau:
        record_info = BS_opt(
            stk_code=stk_code,
            price=df.loc[idx, 'close'],
            amount=300,
            opt='sale',
            record_info=record_info,
            debug=True)

    elif df.loc[idx, 'close'] - record_info['price_last'] < -reseau:
        record_info = BS_opt(
            stk_code=stk_code,
            price=df.loc[idx, 'close'],
            amount=400,
            opt='buy',
            record_info=record_info,
            debug=True)

    else:
        record_info['BS_real'] = 'NO_OPT'

    df.loc[idx, 'strategy_money'] = record_info['amount_remain']*df.loc[idx, 'close'] + record_info['money_remain']
    df.loc[idx, 'origin_money'] = origin_amount*df.loc[idx, 'close']
    df.loc[idx, 'BS'] = record_info['BS_real']
    df.loc[idx, 'amount_remain'] = record_info['amount_remain']
    df.loc[idx, 'money_remain'] = record_info['money_remain']
    df.loc[idx, 'last_price'] = record_info['price_last']


plotOPResult(df)

end = 0