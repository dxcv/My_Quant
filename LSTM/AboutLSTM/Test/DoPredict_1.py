# encoding = utf-8
import tushare as ts

from CornerDetectAndAutoEmail.Sub import genSingleStkTrainData
from LSTM.AboutLSTM.Config import feature_cols, M_INT, N_STEPS, N_INPUTS, HIDDEN_SIZE, NUM_LAYERS, label_col
from LSTM.AboutLSTM.Test.Sub import lstm_model
from SDK.CNN_Data_Prepare import gaussian_normalize, normalize_by_line
import tensorflow as tf
import os
import numpy as np
from pylab import *
import pickle

""" 本脚本根据训练好的lstm模型进行预测 """


""" -------------------- 测试 ---------------------- """
stk_code = '300183'
model_name = '300183_high'

# 准备数据
with open('../DataPrepare/' + stk_code+'testhigh' + '.pkl', 'rb') as f:
    data_test = pickle.load(f)

""" -------------------------- 加载lstm模型进行预测 --------------------------- """

# 创建模型
predictions, loss, train_op, X, y = lstm_model(
    n_steps=N_STEPS,
    n_inputs=len(feature_cols),
    HIDDEN_SIZE=HIDDEN_SIZE,
    NUM_LAYERS=NUM_LAYERS)

# 创建保存器用于模型
saver = tf.train.Saver()

# 初始化
sess = tf.Session()
if os.path.exists('../modelDir/' + model_name + '/' + model_name + '.ckpt.meta'):

    saver = tf.train.import_meta_graph(
        '..\modelDir/' + model_name + '/' + model_name + '.ckpt.meta')
    saver.restore(sess, tf.train.latest_checkpoint(
        '..\modelDir/' + model_name + '/'))

    graph = tf.get_default_graph()

    """ ----------------------- 使用模型进行预测 ------------------------ """
    result = list(map(lambda x: (sess.run([predictions], feed_dict={X: [x[0]]})[0][0][0], x[1][-1][0]), data_test))

    """ -------------------------- 画图展示预测效果 --------------------------- """
    fig, ax = plt.subplots(nrows=1)
    ax_x = list(range(len(result)))
    ax.plot(ax_x, [x[1] for x in result], 'g*--', label='原始数据')
    ax.plot(ax_x, [x[0] for x in result], 'r*--', label='预测数据')

    plt.legend(loc='best')
    plt.show()

else:
    print('lstm模型加载不成功！')

