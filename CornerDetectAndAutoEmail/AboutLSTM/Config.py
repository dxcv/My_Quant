# encoding=utf-8

""" 本脚本包含lstm训练所需要的各种参数 """

feature_cols = ['close', 'M21pre', 'volume', 'MACD', 'RSI5', 'RSI12', 'RSI30', 'SAR', 'slowk', 'slowd', 'upper', 'middle', 'lower', 'MOM']
label_col = ['corner_dist_ratio']

stk_code = 'cyb'
M_INT = 21

N_STEPS = 11
N_INPUTS = len(feature_cols)
HIDDEN_SIZE = 6
NUM_LAYERS = 2