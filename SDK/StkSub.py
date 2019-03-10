# encoding=utf-8

""" 本脚本是用来存储一些与stk息息相关的子函数"""

def getNameByStkCode(stk_info_df, stk_code):

    """
    g_total_stk_info_mysql[g_total_stk_info_mysql['code']=='300183']['name'].values[0]
    根据代码获取名字
    :return:
    """
    if stk_code in ['sh', 'sz', 'cyb', 'zxb']:
        return {
            'sh': '上证指数',
            'sz': '深成指',
            'cyb': '创业板',
            'zxb': '中小板'
        }.get(stk_code)
    else:
        return stk_info_df[stk_info_df['code'] == stk_code]['name'].values[0]