# encoding = utf-8

"""
通过一段时间的波动率对操作价格进行加权，如果波动较大，应该加大操作价格

"""
import math
import tushare as ts
import pandas as pd

from Auto_Report.Auto_Email.Email_SendPdf import dumpPickle
from SDK.DBOpt import genDbConn
from SDK.MyTimeOPT import add_date_str, get_current_date_str
from SendMsgByGUI.QQGUI import send_qq


def calWeight(code):

    """
    9天波动率均值与3日波动率均值的均值为当前波动率加权
    :param code:
    :return:
    """

    df = ts.get_k_data('300183', start=add_date_str(get_current_date_str(), -30))

    # 将昨天的收盘价下移，用来计算波动率
    df['yesterday_close'] = df['close'].shift(1)

    df['rolling'] = df.apply(lambda x: math.fabs(x['high'] - x['low'])*100/x['yesterday_close'], axis=1)
    df['r_3'] = df['rolling'].rolling(window=3).mean()
    df['r_9'] = df['rolling'].rolling(window=9).mean()

    df['r_mean'] = df.apply(lambda x:  (x['r_3'] + x['r_9'])/2, axis=1)

    return df.tail(1)['r_mean'].values[0]


def saveWeightFile():

    """
    将持仓股票的权值存为文件
    :param dir:
    :return:
    """

    # 新方式：lacalDBInfo包括除了“数据库名”之外的其他参数
    localDBInfo = {'host': 'localhost',
                   'port': 3306,
                   'user': 'root',
                   'password': 'ypw1989',
                   'charset': 'utf8'}

    db_name = 'stk_opt_info'

    table_history = 'history'
    table_now = 'now'

    (conn_opt, engine_opt) = genDbConn(localDBInfo, db_name)
    df = pd.read_sql(con=conn_opt, sql='select * from now')

    if not df.empty:
        df['weight'] = df.apply(lambda x: calWeight(x['stk_code']), axis=1)

        dumpPickle(data=df, saveLocation='./Weight/', fileName='weight')
        send_qq('影子', '更新股票的权值成功！\n'+str(df))

    else:
        dumpPickle(data=pd.DataFrame(), saveLocation='./Weight/', fileName='weight')
        send_qq('影子', '更新股票权值时发现 now 表为空！')

    conn_opt.close()


if __name__ == '__main__':

    saveWeightFile()
    r = calWeight('300183')

    end = 0