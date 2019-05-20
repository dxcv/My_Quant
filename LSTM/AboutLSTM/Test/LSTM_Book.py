# encoding=utf-8

"""
本脚本用来测试书上的LSTM代码

"""

import tensorflow as tf
import numpy as np
import pickle
import random
import os
import time

from LSTM.AboutLSTM.Config import N_STEPS, feature_cols, HIDDEN_SIZE, NUM_LAYERS
from LSTM.AboutLSTM.Test.Sub import lstm_model

""" -------------------- 测试 ---------------------- """


def train(data_train, times, model_dir, model_name, N_STEPS, feature_cols, HIDDEN_SIZE, NUM_LAYERS):
    """

    :param times:               训练次数
    :param model_dir:           模型路径        例如：'..\modelDir/'
    :param model_name:          模型名称
    :return:
    """

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
    if os.path.exists(model_dir + model_name + '/' + model_name + '.ckpt.meta'):

        saver = tf.train.import_meta_graph(
            model_dir + model_name + '/' + model_name + '.ckpt.meta')

        saver.restore(sess, tf.train.latest_checkpoint(
            model_dir + model_name + '/'))

        graph = tf.get_default_graph()
    else:
        sess.run(tf.global_variables_initializer())

    loss_list = []
    t_s = time.time()       # 起始时间

    for i in range(times):

        # 从总样本中随机抽取,batch_size = 7
        list_sample = random.sample(data_train, 7)

        input = [x[0] for x in list_sample]
        output = np.reshape([x[1][-1] for x in list_sample], newshape=[-1, 1])

        _, _, l = sess.run([predictions, train_op, loss], feed_dict={X: input, y: output})
        loss_list.append(l)

        if len(loss_list) > 100:

            print('本次损失为：' + str(np.mean(loss_list)))
            loss_list = []

    print('总耗时：' + str((time.time() - t_s)/60))

    # 保存模型
    saver.save(sess=sess, save_path=model_dir + model_name + '/' + model_name + '.ckpt')


if __name__ == '__main__':
    stk_code = '300183'
    data_dir_root = '../DataPrepare/'
    data_dir = data_dir_root+stk_code+'/'

    # 准备数据
    with open(data_dir + stk_code + 'trainhigh' + '.pkl', 'rb') as f:
        data_train_high = pickle.load(f)

    train(
        data_train=data_train_high,
        times=5000000,
        model_dir='..\modelDir/',
        model_name='300183_high',
        N_STEPS=N_STEPS,
        feature_cols=feature_cols,
        HIDDEN_SIZE=HIDDEN_SIZE,
        NUM_LAYERS=NUM_LAYERS)