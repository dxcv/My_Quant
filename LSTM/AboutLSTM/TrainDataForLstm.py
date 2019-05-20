# encoding=utf-8

"""
本脚本用以生成lstm训练用的数据
"""
import math
import tushare as ts
import pickle

from CornerDetectAndAutoEmail.Sub import genSingleStkTrainData, sliceDfToTrainData
from LSTM.AboutLSTM.Config import feature_cols, label_col, N_STEPS
from SDK.CNN_Data_Prepare import gaussian_normalize, normalize
import numpy as np
import os

def genTrainDataHL(stk_code, start_time, N_STEPS, feature_cols, label_col, data_store_dir):
    """
    第二天高低点的判断
    :param stk_code:
    :param start_time:
    :param data_store_dir:       './DataPrepare/'
    :return:
    """

    df_cyb = ts.get_k_data(stk_code, start=start_time)
    df = df_cyb

    # 计算标签的环比变化率
    df[label_col[0] + '_last'] = df[label_col[0]].shift(-1)
    df[label_col[0]+'_ratio'] = df.apply(lambda x: x[label_col[0]]/x[label_col[0] + '_last'], axis=1)

    df[label_col[0]+'_next'] = df[label_col[0]+'_ratio'].shift(1)

    # 删除空值
    df = df.dropna(how='any')

    # 对数据进行切片
    data_slice_list = sliceDfToTrainData(
        df=df,
        length=N_STEPS-1,
        feature_cols=feature_cols,
        label_col=[label_col[0]+'_next'],
        norm_flag=False
    )

    # 对数据进行特定的归一化操作，h/l/c三个维度进行统一的归一化
    data_slice_list_norm = list(map(lambda x:
                               (np.hstack((normalize(x[0][:, :-1]), normalize(x[0][:, [-1]]))), x[1]),
                               data_slice_list
                               ))

    # 将数据分割为训练集和数据集
    lenth = math.floor(len(data_slice_list_norm)*0.8)
    list_train = data_slice_list_norm[:lenth]
    list_test = data_slice_list_norm[lenth:]

    if not os.path.exists(data_store_dir):
        os.makedirs(data_store_dir)

    # 保存数据
    with open(data_store_dir + stk_code + 'train' + label_col[0] + '.pkl', 'wb') as f:
        pickle.dump(list_train, f)

    with open(data_store_dir + stk_code + 'test' + label_col[0] + '.pkl', 'wb') as f:
        pickle.dump(list_test, f)


if __name__ == '__main__':
    genTrainDataHL(stk_code='300183',
                   start_time='2012-01-01',
                   N_STEPS=N_STEPS,
                   feature_cols=feature_cols,
                   label_col=['low'],
                   data_store_dir='./DataPrepare/300183/')

    genTrainDataHL(stk_code='300183',
                   start_time='2012-01-01',
                   N_STEPS=N_STEPS,
                   feature_cols=feature_cols,
                   label_col=['high'],
                   data_store_dir='./DataPrepare/300183/')