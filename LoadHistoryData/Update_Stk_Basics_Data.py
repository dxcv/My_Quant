# encoding = utf-8

from General.GlobalSetting import *
from SDK.SDKHeader import *

'''
每天下载，数据格式为df，命名为“stk_basics”+current date
'''

def update_stk_basics():
    current_date = get_current_date_str()

    if not is_table_exist(conn=conn_stkBasics,database_name=stk_stkBasics_data_db_name,table_name='stk_basics'+current_date):
        ts.get_stock_basics()