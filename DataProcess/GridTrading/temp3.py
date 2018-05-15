# encoding = utf-8

from General.GlobalSetting import *
from SDK.SDKHeader import *

# 获取原始数据
stk_df = get_total_table_data(conn_k,'k000625')

# 计算均值
stk_df['close_20'] = stk_df['close'].rolling(window=20).mean()

fig,ax = subplots(ncols=1,nrows=2)

ax[0].plot(stk_df['close'],'g*--',label='close',linewidth=0.5,markersize=1)
ax[0].plot(stk_df['close_20'],'r*--',label='close_20',linewidth=0.5,markersize=1)

ax[0].grid()
ax[1].plot(stk_df['close'] - stk_df['close_20'],'r*--',label='close_diff',linewidth=0.5,markersize=1)
ax[1].grid()

plt.show()

end = 0
