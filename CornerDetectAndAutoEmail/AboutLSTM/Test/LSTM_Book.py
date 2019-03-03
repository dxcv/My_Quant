# encoding=utf-8

"""
本脚本用来测试书上的LSTM代码

"""

import tensorflow as tf
import numpy as np
import pickle
import random
import os
from CornerDetectAndAutoEmail.AboutLSTM.Test.Sub import lstm_model



""" -------------------- 测试 ---------------------- """
stk_code = 'cyb'

# 准备数据
with open('../DataPrepare/' + stk_code + '.pkl', 'rb') as f:
    data_train = pickle.load(f)

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
else:
    sess.run(tf.global_variables_initializer())

loss_list = []
for i in range(500000):

    # 从总样本中随机抽取,batch_size = 7
    list_sample = random.sample(data_train, 7)

    input = [x[0] for x in list_sample]
    output = np.reshape([x[1][-1] for x in list_sample], newshape=[-1, 1])

    _, _, l = sess.run([predictions, train_op, loss], feed_dict={X: input, y: output})
    loss_list.append(l)

    if len(loss_list) > 100:

        print('本次损失为：' + str(np.mean(loss_list)))
        loss_list = []

# 保存模型
saver.save(sess=sess, save_path='../modelDir/LstmForCornerPot.ckpt')