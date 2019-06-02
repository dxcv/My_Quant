# encoding=utf-8

import pandas as pd
import tushare as ts

from SDK.MyTimeOPT import get_current_date_str, add_date_str

"""
计算相对排名

"""


def relativeRand(v_total, v_now):
    """
    计算相对排名子函数
    :param list:
    :return:
    """
    if isinstance(v_total, pd.Series):
        v_total = list(v_total.values)
    else:
        v_total = list(v_total)

    # 计算排名
    v_bigger_amount = len(list(filter(lambda x: x > v_now, v_total)))

    return v_bigger_amount/(len(v_total)+0.000001)*100


def calSingleStkRank(m_days, stk_code, days_length, p_now):

    """
    :param m_days:              ？天均线的离心度
    :param stk_code:
    :param days_length:         在？天内进行排名
    :return:
    """

    df = ts.get_k_data(stk_code, start=add_date_str(get_current_date_str(), -1*days_length*1.8))

    if len(df) < days_length*0.8:
        print('函数 calSingleStkRank: 该stk历史数据不足！')
        return -1

    # 测试相对均值偏移度
    df['m9'] = df['close'].rolling(window=m_days).mean()
    df['diff_m9'] = df.apply(lambda x: x['close'] - x['m9'], axis=1)

    """
    df.plot('date', ['close', 'diff_m9', 'rank'], subplots=True)
    """

    # 给m9打分
    return relativeRand(df['diff_m9'], p_now)


if __name__ == '__main__':

    df = ts.get_k_data('603421')

    # 测试相对均值偏移度
    df['m9'] = df['close'].rolling(window=9).mean()
    df['diff_m9'] = df.apply(lambda x: x['close'] - x['m9'], axis=1)

    """
    df.plot('date', ['close', 'diff_m9', 'rank'], subplots=True)
    """

    # 给m9打分
    df['rank'] = df.apply(lambda x: relativeRand(df['diff_m9'], x['diff_m9']), axis=1)

end = 0