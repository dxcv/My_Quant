# encoding=utf-8

import pandas as pd
import tushare as ts


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


if __name__ == '__main__':

    df = ts.get_k_data('000001')
    r = relativeRand(df['close'], df.tail(1)['close'].values[0])

    # 测试相对均值偏移度
    df['m9'] = df['close'].rolling(window=9).mean()
    df['diff_m9'] = df.apply(lambda x: x['close'] - x['m9'], axis=1)

    """
    df.plot('date', ['close', 'diff_m9', 'rank'], subplots=True)
    """

    # 给m9打分
    df['rank'] = df.apply(lambda x: relativeRand(df['diff_m9'], x['diff_m9']), axis=1)

end = 0