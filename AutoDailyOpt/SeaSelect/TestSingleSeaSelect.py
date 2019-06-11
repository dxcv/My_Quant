# encoding=utf-8

"""
测试海选过程中单个stk的正确性
"""
from General.AutoStkConfig import SeaSelectDataPWD
from RelativeRank.Sub import calRealtimeRank, saveStkMRankHistoryData

stk_code = '600801'

# 准备数据
saveStkMRankHistoryData(stk_code=stk_code, history_days=400, m_days=9, save_dir=SeaSelectDataPWD+'/stk_pool_data/')

# 进行计算
r = calRealtimeRank(
    stk_code=stk_code,
    M_days=9,
    history_data_dir=SeaSelectDataPWD + '/stk_pool_data/')