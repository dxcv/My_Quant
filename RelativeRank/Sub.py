# encoding=utf-8

import pandas as pd
import tushare as ts
import numpy as np
import os

from Auto_Report.Auto_Email.Email_SendPdf import dumpPickle
from SDK.MyTimeOPT import get_current_date_str, add_date_str
from General.AutoStkConfig import stk_list
from SDK.PickleSaveSub import dumpP, loadP
from SendMsgByGUI.QQGUI import send_qq



"""
计算相对排名

"""

MDataPWD = os.getcwd()

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


def saveStkMRankHistoryData(stk_code, history_days, m_days, save_dir):
    """
    保存stk的历史数据，用来实时计算均线离心度分数

    :param stk_code:
    :param history_days:
    :param save_dir:        './M_data/'
    :return:
    """
    try:

        df = ts.get_k_data(stk_code, start=add_date_str(get_current_date_str(), -1*history_days*1.8))

        if len(df) < history_days*0.8:
            print('函数 calSingleStkRank: 该stk历史数据不足！')
            return -1

        # 测试相对均值偏移度
        df['m9'] = df['close'].rolling(window=m_days).mean()
        df['diff_m9'] = df.apply(lambda x: x['close'] - x['m9'], axis=1)

        df = df.dropna()

        dict_restore = {
            'stk_code': stk_code,
            'history_M_diverge_data': list(df['diff_m9'].values),
            'latest_data': list(df.tail(m_days-1)['close'].values),
            'update_date': df.tail(1)['date'].values[0]
        }

        dumpP(
            data=dict_restore,
            saveLocation=save_dir,
            fileName=stk_code+'_M'+str(m_days))

        return 0

    except:
        return 1


def calRealtimeRank(stk_code, M_days, history_data_dir):
    """
    计算一只stk的离心度名次
    :param stk_code:
    :param M_days:
    :param history_data_dir: './M_data/'
    :return:
    """

    # 加载数据测试
    dict = loadP(
        loadLocation=history_data_dir,
        fileName=stk_code+'_M'+str(M_days))

    # 获取实时价格
    current_price = float(ts.get_realtime_quotes(stk_code)['price'].values[0])

    # 计算实时偏离度
    list_history = dict['latest_data']
    list_history.append(current_price)
    M_diff = current_price - np.mean(list_history)

    # 计算排名
    return relativeRand(dict['history_M_diverge_data'], M_diff)


def checkDivergeLowLevel():
    """
    供定时器调用的回调函数，按频率检查关心的stk的，对高于80分的进行提示
    :return:
    """
    for stk in stk_list:

        r = calRealtimeRank(
            stk_code=stk,
            M_days=9,
            history_data_dir=MDataPWD+'/M_data/')

        if r > 80:
            send_qq('影子', 'Attention：\n'+stk+'趋向高分！分数为：'+str('%0.2f') % r)
        else:
            print(stk+'分数处于正常状态！分数为：'+str('%0.2f') % r)


def updateConcernStkMData():
    """
    定时器定时调用，更新各stk的M离心度历史数据
    :return:
    """
    try:
        for stk in stk_list:
            saveStkMRankHistoryData(stk_code=stk, history_days=400, m_days=9, save_dir='./M_data/')
            send_qq('影子', '更新' + stk + '离心度历史数据成功！')
    except:
        send_qq('影子', '更新离心度历史数据失败！')


if __name__ == '__main__':
    # r = getMDataPWD()

    updateConcernStkMData()
    checkDivergeLowLevel()

end = 0