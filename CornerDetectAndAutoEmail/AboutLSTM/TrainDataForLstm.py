# encoding=utf-8

"""
本脚本用以生成lstm训练用的数据
"""
import tushare as ts
import pickle

from CornerDetectAndAutoEmail.Sub import genSingleStkTrainData, sliceDfToTrainData
from SDK.CNN_Data_Prepare import gaussian_normalize

stk_code = 'cyb'
df_cyb = ts.get_k_data(stk_code)
df = genSingleStkTrainData(
    stk_K_df=df_cyb,
    M_int=21,
    stk_code=stk_code,
    stk_name=stk_code
)

feature_cols = ['close', 'volume', 'MACD', 'RSI5', 'RSI12', 'RSI30', 'SAR', 'slowk', 'slowd']
label_col = ['corner_dist_ratio']

# 对相应的数据进行归一化
for col in feature_cols:
    df[col] = gaussian_normalize(df[col])

# 将标签下移一位，用于预测未来
df[label_col[0]] = df[label_col[0]].shift(-1)

# 删除空值
df = df.dropna(how='any')

# 对数据进行切片
data_slice_list = sliceDfToTrainData(
    df=df,
    length=7,
    feature_cols=feature_cols,
    label_col=label_col
)

# 保存数据
with open('./DataPrepare/' + stk_code +'.pkl', 'wb') as f:
    pickle.dump(data_slice_list, f)