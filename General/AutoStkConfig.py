# encoding=utf-8
"""
这个脚本是用来存储 stk自动检测 程序的配置信息

"""

cubic_test_last_step = 7        # 在曲线拟合时，取最后的几个值进行二次拟合

# pic_save_dir_root = 'C:/Users/paul/Desktop/软件代码/Git-Clone/TempPicStore/'

pic_save_dir_root = 'F:/软件代码/Git-Clone/TempPicStore/'

plot_current_days_amount = 40   # 画出近期的stk走势情况，该参数指示最近取的天数


# 关心的stk
stk_list = [
    'cyb',
    'sh',
    'sz',
    '300183'
]

step_corner_detect = 6    # 在判断拐点的时候，取最近的数据的个数