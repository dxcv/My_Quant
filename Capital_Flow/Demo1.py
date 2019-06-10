# encoding=utf-8

import jqdatasdk as jq
from JQData_Test.auth_info import *

"""

"""

df_flow = get_money_flow('300183.XSHE', '2019-05-01', '2019-06-10')
df_flow_plot = df_flow.loc[:, [x not in ['sec_code'] for x in df_flow.columns.values]]



end = 0

"""
df_flow_plot.plot('date', list(df_flow.columns.values).remove('date'), subplots=True)
"""
