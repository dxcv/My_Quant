# encoding = utf-8
import tushare as ts

from CornerDetectAndAutoEmail.AboutLSTM.Test.Sub import lstm_model
from CornerDetectAndAutoEmail.Sub import genSingleStkTrainData
from SDK.CNN_Data_Prepare import gaussian_normalize
import tensorflow as tf
import os
import numpy as np
from pylab import *


"""
本脚本根据训练好的lstm模型进行预测

"""


""" ---------------------------- 准备数据 ----------------------------- """

stk_code = 'cyb'
df_cyb = ts.get_k_data(stk_code, start='2010-01-01', end='2015-03-03')
df = genSingleStkTrainData(
    stk_K_df=df_cyb,
    M_int=21,
    stk_code=stk_code,
    stk_name=stk_code
)

feature_cols = ['close', 'volume', 'MACD', 'RSI5', 'RSI12', 'RSI30', 'SAR', 'slowk', 'slowd']
label_col = ['corner_dist_ratio']

# 取出标签数据
df = df.loc[:, feature_cols+label_col]


# 对相应的数据进行归一化
for col in feature_cols:
    df[col] = gaussian_normalize(df[col])

df = df.reset_index(drop=True)


""" -------------------------- 加载lstm模型进行预测 --------------------------- """

# 创建模型
predictions, loss, train_op, X, y = lstm_model(
    n_steps=8,
    n_inputs=9,
    HIDDEN_SIZE=6,
    NUM_LAYERS=2)

# 创建保存器用于模型
saver = tf.train.Saver()

# 初始化
sess = tf.Session()
if os.path.exists('../modelDir/LstmForCornerPot.ckpt.meta'):

    saver = tf.train.import_meta_graph(
        '..\modelDir\LstmForCornerPot.ckpt.meta')
    saver.restore(sess, tf.train.latest_checkpoint(
        '..\modelDir/'))

    graph = tf.get_default_graph()

    """ ---------------------- 使用模型进行预测 ------------------------- """
    for idx in df.loc[10:, :].index:
        ipt = df.loc[idx - 7:idx, feature_cols].values
        pre = sess.run([predictions], feed_dict={X: [ipt]})[0][0][0]

        df.loc[idx, 'pre'] = pre

    """ -------------------------- 画图展示预测效果 -------------------- """
    fig, ax = plt.subplots(nrows=3)
    ax[0].plot(df.index, df['corner_dist_ratio'], 'g*--', label='原始数据')
    ax[0].plot(df.index, np.zeros(len(df.index)), 'b-')

    ax[1].plot(df.index, df['pre'].fillna(0), 'r*--', label='预测数据')
    ax[1].plot(df.index, np.zeros(len(df.index)), 'b-')

    ax[2].plot(df.index, df['close'], 'g*--', label='收盘价')
    for ax_sig in ax:
        plt.legend(loc='best')

    plt.show()

    end = 0






else:
    print('lstm模型加载不成功！')

