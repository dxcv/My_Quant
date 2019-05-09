# encoding=utf-8

import tushare as ts
from CornerDetectAndAutoEmail.Sub import genSingleStkTrainData
from LSTM.AboutLSTM.Config import feature_cols, M_INT, N_STEPS, N_INPUTS, HIDDEN_SIZE, NUM_LAYERS, label_col
from LSTM.AboutLSTM.Test.Sub import lstm_model
from SDK.CNN_Data_Prepare import gaussian_normalize, normalize_by_line, normalize
import tensorflow as tf
import os
import numpy as np
from pylab import *
import pickle

"""
本脚本实现调用model预测totorrow的high点 

"""

""" ---------------------- 参数准备 ---------------------- """
stk_code = '300183'
model_dir = '../modelDir/'

""" ---------------------- 获取实时数据 ---------------------- """
data_now = ts.get_k_data(stk_code)[-11:]

# 准备输入数据
input_values = data_now.loc[:, feature_cols].values

# 进行归一化
input_normal = np.hstack((normalize(input_values[:, :3]), normalize(input_values[:, [3]])))

""" ---------------------- 创建模型 ---------------------- """
predictions, loss, train_op, X, y = lstm_model(
    n_steps=N_STEPS,
    n_inputs=len(feature_cols),
    HIDDEN_SIZE=HIDDEN_SIZE,
    NUM_LAYERS=NUM_LAYERS)

# 创建保存器用于模型
saver = tf.train.Saver()

model_name = '300183_high'

# 初始化
sess = tf.Session()
if os.path.exists(model_dir + model_name + '/' + model_name + '.ckpt.meta'):

    saver = tf.train.import_meta_graph(
        model_dir + model_name + '/' + model_name + '.ckpt.meta')
    saver.restore(sess, tf.train.latest_checkpoint(
        model_dir + model_name + '/'))

    graph = tf.get_default_graph()

    high_ratio = sess.run([predictions], feed_dict={X: [input_normal]})[0][0][0]
    high = data_now.tail(1).loc[:, 'high'].values[0] * high_ratio

else:
    print('加载模型' + model_name + '失败！')
    high = -1

model_name = '300183_low'
if os.path.exists(model_dir + model_name + '/' + model_name + '.ckpt.meta'):

    saver = tf.train.import_meta_graph(
        model_dir + model_name + '/' + model_name + '.ckpt.meta')
    saver.restore(sess, tf.train.latest_checkpoint(
        model_dir + model_name + '/'))

    graph = tf.get_default_graph()

    low_ratio = sess.run([predictions], feed_dict={X: [input_normal]})[0][0][0]
    low = data_now.tail(1).loc[:, 'low'].values[0]*low_ratio

else:
    print('加载模型' + model_name + '失败！')
    low = -1

print('high:'+str(high)+'   low:'+str(low))

end = 0
