# encoding = utf-8
from General.GlobalSetting import *

'''绘制以dataframe的date列为横轴，给定列为纵轴的图
y_axis_info范例：

“列名” “颜色线条属性”  “注释字符串”
[
("mean10","go--",U"10日均值"),
("mean20","k*--",U"20日均值"),
("mean10","ro--",U"10日均值"),
("mean20","b*--",U"20日均值"),
("mean10","yo--",U"10日均值"),
("mean20","m*--",U"20日均值")
]
'''
def plot_x_date(code_param,data_df_param,y_axis_info_param):

    ave_df_param = data_df_param.sort_values(by='date',ascending=True)

    # trick to get the axes
    fig, ax = plt.subplots()

    x_axis = range(0, len(ave_df_param['date']))
    for y_axis_info in y_axis_info_param:
        ax.plot(x_axis, ave_df_param[y_axis_info[0]], y_axis_info[1], label=y_axis_info[2])

    xticklabels = list(ave_df_param['date'])
    ax.set_xticklabels(xticklabels, rotation=90)
    ax.set_title('stk'+code_param)
    ax.legend(loc='best')
    plt.show()


def addXticklabel(ax, df_date_S, x_amount, fontsize=5, rotation=90):

    """
    将字符串列用作x轴标签
    :param ax:
    :param df_date_S:   sh_index['date']
    :param x_amount:    x轴最多40个label，多了太密
    :return:
    """
    xticks = range(0, len(df_date_S), int(math.ceil(len(df_date_S) / x_amount)))
    xticklabels_all_list = list(df_date_S.sort_values(ascending=True))
    xticklabels_all = [xticklabels_all_list[n] for n in xticks]

    ax.set_xticks(xticks)
    ax.set_xticklabels(xticklabels_all, rotation=rotation, fontsize=fontsize)

    return ax


