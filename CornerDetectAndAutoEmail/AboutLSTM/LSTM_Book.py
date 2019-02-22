# encoding=utf-8

"""
本脚本用来测试书上的LSTM代码

"""

import tensorflow as tf
import numpy as np


def lstm_model(X, y, is_training, HIDDEN_SIZE, NUM_LAYERS):

    cell = tf.nn.rnn_cell.MultiRNNCell(
        [tf.nn.rnn_cell.BasicLSTMCell(HIDDEN_SIZE) for _ in range(NUM_LAYERS)]
    )

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
        loss, tf.train.get_global_step(), optimizer='Adagrad', learning_rate=0.1
    )

    return predictions, loss, train_op


""" -------------------- 测试 ---------------------- """
sess = tf.Session()


predictions, loss, train_op = lstm_model(np.random.)
