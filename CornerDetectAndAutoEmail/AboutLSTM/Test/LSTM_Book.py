# encoding=utf-8

"""
本脚本用来测试书上的LSTM代码

"""

import tensorflow as tf
import numpy as np
import pickle
import random
import os

def lstm_model(n_steps, n_inputs, HIDDEN_SIZE, NUM_LAYERS):

    """

    :param n_steps:
    :param n_inputs:
    :param HIDDEN_SIZE:
    :param NUM_LAYERS:
    :return:
    """

    cell = tf.nn.rnn_cell.MultiRNNCell(
        [tf.nn.rnn_cell.BasicLSTMCell(HIDDEN_SIZE) for _ in range(NUM_LAYERS)]
    )

    X = tf.placeholder(tf.float32, [None, n_steps, n_inputs], name='ipt')
    y = tf.placeholder(tf.float32, [None, 1], name='opt')

    """
    使用tf自带接口将多层LSTM连接成RNN网络，并计算前向结果
    outputs 的维度是：[batch_size, time, HIDDEN_SIZE]
    """
    outputs, _ = tf.nn.dynamic_rnn(cell, X, dtype=tf.float32)

    """ 在实例中我们只取预测数据的最后一个 """
    output = outputs[:, -1, :]

    """ 增加一层全连接层作为输出 """
    predictions = tf.contrib.layers.fully_connected(output, 1, activation_fn=None)

    """定义损失 """
    loss = tf.losses.mean_squared_error(labels=y, predictions=predictions)

    """ 创建优化器并得到优化步骤 """
    train_op = tf.contrib.layers.optimize_loss(
        loss,
        tf.train.get_global_step(),
        optimizer='Adagrad',
        learning_rate=0.1,
        name='optimize'
    )

    return predictions, loss, train_op, X, y


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
    NUM_LAYERS=1)

# 创建保存器用于模型
saver = tf.train.Saver()

# 初始化
sess = tf.Session()
if os.path.exists('F:\MYAI\Code\master\My_Quant\CornerDetectAndAutoEmail\AboutLSTM\modelDir\LstmForCornerPot.ckpt.meta'):

    saver = tf.train.import_meta_graph(
        'F:\MYAI\Code\master\My_Quant\CornerDetectAndAutoEmail\AboutLSTM\modelDir\LstmForCornerPot.ckpt.meta')

    saver.restore(sess, tf.train.latest_checkpoint(
        'F:\MYAI\Code\master\My_Quant\CornerDetectAndAutoEmail\AboutLSTM\modelDir/'))

    graph = tf.get_default_graph()
else:
    sess.run(tf.global_variables_initializer())

loss_list = []
for i in range(500000):

    # 从总样本中随机抽取,batch_size = 7
    list_sample = random.sample(data_train, 7)

    input = [x[0] for x in list_sample]
    output = np.reshape([x[1][-1] for x in list_sample], newshape=[-1, 1])

    _, l = sess.run([train_op, loss], feed_dict={X: input, y: output})
    loss_list.append(l)

    if len(loss_list)>100:

        print('本次损失为：' + str(np.mean(loss_list)))
        loss_list = []

# 保存模型
saver.save(sess=sess, save_path='../modelDir/LstmForCornerPot.ckpt')