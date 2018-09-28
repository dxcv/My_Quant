from jqdatasdk import query, valuation, income
from General.GlobalSetting import *
from JQData_Test.auth_info import *


def get_indus_stk_df(stk_list, year):

    return jqdatasdk.get_fundamentals(query(
              valuation, income
          ).filter(
              # 这里不能使用 in 操作, 要使用in_()函数
              valuation.code.in_(stk_list)
          ), statDate=year)


def plot(indus_name, data_list, year_list):

    fig, ax = plt.subplots()
    ax.plot(year_list,data_list,'g*--')
    ax.set_title(indus_name + ' 行业 年度 总净利润')
    plt.savefig('./indus_pic_dir/'+indus_name+'.png')

# 年份列表
year_list = list(range(2010,2018))


# 获取申万一级行业分类
indus = jqdatasdk.get_industries(name='sw_l1')

indus_dic = [{'indus_code':x,
              'indus_name':indus.loc[x,'name'],
              'indus_stk':jqdatasdk.get_industry_stocks(industry_code=x)
              } for x in indus.index]

# 向字典列表中增加各行业所含股票的数据，df格式
for dic in indus_dic:
    dic['stk_df_list'] = [get_indus_stk_df(dic['indus_stk'], x) for x in year_list]
    dic['net_profit_list'] = [x['net_profit'].sum() for x in dic['stk_df_list']]

    # 将增长曲线图打印
    plot(dic['indus_name'],dic['net_profit_list'],year_list)




end = 0