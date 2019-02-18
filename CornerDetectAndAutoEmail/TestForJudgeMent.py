#encoding=utf-8
import talib
import tushare as ts

from CornerDetectAndAutoEmail.Sub import JudgeCornerPot, IsPotInCurveMedian
from General.AutoStkConfig import cubic_test_last_step, tailLengthForMacd
from SDK.MyTimeOPT import DateStr2Sec
from pylab import *

"""
本脚本用于测试拐点判断准确性
"""
sh_index = ts.get_k_data(code='300183', start='2018-01-01')

# 按升序排序
stk_df = sh_index.sort_values(by='date', ascending=True)

# 后验拐点用数据长度的一般
corner_Pot_Retrospective_Half = 6


sh_index = stk_df
stk_df_addInfo = stk_df

for idx in sh_index.loc[tailLengthForMacd:, :].index:
    df_part = sh_index.loc[idx-tailLengthForMacd:idx, :]

    # 获取当前时间并先验拐点
    current_date = df_part.tail(1)['date'].values[0]
    judge_result = JudgeCornerPot(df_part, '300183', current_date, debug=True)

    # 存储结果
    stk_df_addInfo.loc[idx, 'corner_flag'] = judge_result['corner_flag']
    stk_df_addInfo.loc[idx, 'err'] = judge_result['err']

    if judge_result['corner_flag']:
        print(current_date+'：这一天是拐点！')
    else:
        print(current_date + '：这一天不是拐点！')


stk_df['MACD'], stk_df['MACDsignal'], stk_df['MACDhist'] = talib.MACD(stk_df.close,
                                                                                fastperiod=12, slowperiod=26,
                                                                                signalperiod=9)


# 计算后验拐点
for idx in stk_df.loc[corner_Pot_Retrospective_Half:len(stk_df)-corner_Pot_Retrospective_Half, :].index:

    # 进行二次曲线拟合
    r = IsPotInCurveMedian(y_axis=stk_df.loc[idx-corner_Pot_Retrospective_Half:idx+corner_Pot_Retrospective_Half, 'MACD'], median_neighbourhood=0.1)

    stk_df.loc[idx, 'corner_flag_A'] = r['corner_flag']
    stk_df.loc[idx, 'err'] = r['err']


# 计算收盘价均线，根据均线计算拐点
stk_df['M21'] = stk_df['close'].rolling(window=21, center=True).mean()


# 求解均线拐点
for idx in stk_df.loc[corner_Pot_Retrospective_Half:len(stk_df)-corner_Pot_Retrospective_Half, :].index:

    # 进行二次曲线拟合
    r = IsPotInCurveMedian(y_axis=stk_df.loc[idx-corner_Pot_Retrospective_Half:idx+corner_Pot_Retrospective_Half, 'M21'], median_neighbourhood=0.1)

    stk_df.loc[idx, 'corner_flag_M21'] = r['corner_flag']
    stk_df.loc[idx, 'err_M21'] = r['err']

# 取出秒数轴用于后续的横坐标
stk_df['second'] = stk_df.apply(lambda x: DateStr2Sec(x['date']), axis=1)

# 画图展示效果
sh_index = stk_df

fig, ax = plt.subplots(nrows=3, ncols=1)

df_normal = sh_index[sh_index.corner_flag==False]
# x_normal_axis = list(map(lambda x: DateStr2Sec(x), df_normal['date']))
ax[0].plot(df_normal['second'], df_normal['MACD'],  'g*')

df_corner = sh_index[sh_index.corner_flag==True]
# x_corner_axis = list(map(lambda x: DateStr2Sec(x), df_corner['date']))
ax[0].plot(df_corner['second'], df_corner['MACD'],  'r*')

# 打印后验拐点
df_normal_A = sh_index[sh_index.corner_flag_A==False]
# x_normal_axis = list(map(lambda x: DateStr2Sec(x), df_normal_A['date']))
ax[1].plot(df_normal_A['second'], df_normal_A['MACD'],  'g*')


df_corner_A = sh_index[sh_index.corner_flag_A==True]
# x_corner_axis = list(map(lambda x: DateStr2Sec(x), df_corner_A['date']))
ax[1].plot(df_corner_A['second'], df_corner_A['MACD'],  'r*')


# 打印中心10均线
ax[2].plot(sh_index['second'], sh_index['M21'],  'g*')
M21Corner = sh_index[sh_index['corner_flag_M21']==True]
ax[2].plot(M21Corner['second'], M21Corner['M21'],  'r*')


# plot data
plt.show()

end = 0