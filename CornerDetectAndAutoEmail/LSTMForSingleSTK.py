#encoding=utf-8

import tushare as ts

from CornerDetectAndAutoEmail.Sub import genSingleStkTrainData, sliceDfToTrainData
from SDK.CNN_Data_Prepare import gaussian_normalize
from SDK.LSTM_Class import LSTMRNN
import tensorflow as tf

from SDK.MyTimeOPT import get_current_date_str
import numpy as np

"""
本脚本所做：
1、生成由指标和拐点组成的训练数据
2、尝试使用LSTM进行训练
"""

""" ----------------------- 准备数据 ----------------------------- """

feature_cols = ['close', 'volume', 'MACD', 'RSI5', 'RSI12', 'RSI30', 'SAR', 'slowk', 'slowd']
label_col = ['corner_dist_ratio']

df_cyb = ts.get_k_data('cyb')
df = genSingleStkTrainData(
    stk_K_df=df_cyb,
    M_int=21,
    stk_code='cyb',
    stk_name='cyb'
)

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

""" ---------------------- 创建lstm模型并进行训练 ------------------------- """

# 1、创建模型
model = LSTMRNN(
    n_steps=8,
    input_size=len(feature_cols),
    output_size=len(label_col),
    cell_size=6,
    batch_size=1)

sess = tf.Session()

# 创建保存器用于模型
saver = tf.train.Saver()

# 将可视化数据写入文件（可有可无）
merged = tf.summary.merge_all()
writer = tf.summary.FileWriter(r'logs/', tf.get_default_graph())

# 2、进行初始化
sess.run(tf.global_variables_initializer())

# 开始训练
for times in range(0, 10000):

    err = []
    for s in data_slice_list:

        # 构造输入字典：feed_dict是TensorFlow世界与外界的数据通道！
        feed_dict = {
            model.xs: [s[0]],
            model.ys: [s[1]],
        }

        # 进行训练
        _, cost, state, pred = sess.run(
            [model.train_op, model.cost, model.cell_final_state, model.pred],
            feed_dict=feed_dict)

        err.append(cost)

    # 打印损失
    print('本次损失为：'+str(np.mean(err)))

# 保存模型
saver.save(sess=sess, save_path='./modelDir/' + 'lstmModel' + get_current_date_str() + '.ckpt')

end=0