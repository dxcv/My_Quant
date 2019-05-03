# encoding=utf-8

"""
本脚本用以生成lstm训练用的数据
"""
import math
import tushare as ts
import pickle

from CornerDetectAndAutoEmail.Sub import genSingleStkTrainData, sliceDfToTrainData
from LSTM.AboutLSTM.Config import feature_cols, label_col, N_STEPS
from SDK.CNN_Data_Prepare import gaussian_normalize

stk_code = 'cyb'
df_cyb = ts.get_k_data(stk_code, start='2010-01-01')
# df = genSingleStkTrainData(
#     stk_K_df=df_cyb,
#     M_int=21,
#     stk_code=stk_code,
#     stk_name=stk_code
# )

df = df_cyb

# 计算标签的环比变化率

df[label_col[0] + '_last'] = df[label_col[0]].shift(-1)
df[label_col[0]+'_ratio'] = df.apply(lambda x: x[label_col[0]]/x[label_col[0] + '_last'], axis=1)

df[label_col[0]+'_next'] = df[label_col[0]+'_ratio'].shift(1)

# 对相应的数据进行归一化
# for col in feature_cols:
#     df[col] = gaussian_normalize(df[col])


# 删除空值
df = df.dropna(how='any')

# 对数据进行切片
data_slice_list = sliceDfToTrainData(
    df=df,
    length=N_STEPS-1,
    feature_cols=feature_cols,
    label_col=[label_col[0]+'_next'],
    norm_flag=True
)

# 将数据分割为训练集和数据集
lenth = math.floor(len(data_slice_list)*0.8)
list_train = data_slice_list[:lenth]
list_test = data_slice_list[lenth:]

# 保存数据
with open('./DataPrepare/' + stk_code+'train' + '.pkl', 'wb') as f:
    pickle.dump(list_train, f)

with open('./DataPrepare/' + stk_code+'test' + '.pkl', 'wb') as f:
    pickle.dump(list_test, f)