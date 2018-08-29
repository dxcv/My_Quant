# encoding = utf-8

from SDK.SDKHeader import *
import random

import pandas as pd
import numpy as np
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.legends import Legend

from reportlab.lib.pagesizes import letter

from reportlab.platypus import *
from reportlab.lib.styles import getSampleStyleSheet

# 画图相关
from reportlab.graphics.shapes import Drawing, PolyLine, colors, Auto
from reportlab.graphics import renderPDF
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.graphics.widgets.markers import makeMarker


from reportlab.pdfbase.pdfmetrics import stringWidth

from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

pdfmetrics.registerFont(TTFont('song', 'SURSONG.TTF'))
pdfmetrics.registerFont(TTFont('hei', 'SIMHEI.TTF'))

from reportlab.lib import fonts
fonts.addMapping('song', 0, 0, 'song')
fonts.addMapping('song', 0, 1, 'song')
fonts.addMapping('song', 1, 0, 'hei')
fonts.addMapping('song', 1, 1, 'hei')


def addFront(canvas_param, theme, subtitle, pagesize=letter):
    """
    函数功能：为pdf文档添加功能，分“主题”、“副标题”两部分
    :param canvas:
    :param pagesize: 页面大小，默认A4
    :param theme: 主题字符串
    :param subtitle: 副标题字符串
    :return:
    """
    PAGE_WIDTH = pagesize[0]
    PAGE_HEIGHT = pagesize[1]

    # 设置主标题字体并打印主标题
    canvas_param.setFont("song", 30)
    canvas_param.drawString((PAGE_WIDTH-stringWidth(theme, fontName='song', fontSize=30))/2.0, PAGE_HEIGHT*0.618, theme)

    # 设置副标题字体并打印副标题
    canvas_param.setFont("song", 10)
    canvas_param.drawString((PAGE_WIDTH-stringWidth(theme, fontName='song', fontSize=30))/2.0, PAGE_HEIGHT*0.15, subtitle)

    canvas_param.showPage()

    return canvas_param


def add_legend(draw_obj, chart, pos_x, pos_y):

    """
    函数功能：voltGroupDisplayByBar函数的子函数
    :param draw_obj:
    :param chart:
    :return:
    """
    legend = Legend()
    legend.alignment = 'right'
    legend.fontName = 'song'
    legend.x = pos_x
    legend.y = pos_y
    legend.colorNamePairs = Auto(obj=chart)
    draw_obj.add(legend)


def ExtractPointFromDf_DateX(df_origin, date_col, y_col):

    """
    函数功能：从一个dataframe中提取两列，组成point列表格式，以供ReportLab画图之用
                同时将日期中的时间提取出来，转为秒。

                本函数主要用来画当日数据！因为将datetime中的date去掉了，只保留time。

    :param df_origin:
    :param x_col:
    :param y_col:
    :return:
    """

    # 将“data”列中的数据解析后，作为新的列增加到df中
    # df_origin = ExtractJsonToColum(df_row=df_origin, col='data')
    # if len(df_origin) == 0:
    #     return []

    # 按时间排序，并删除空值
    df_origin = df_origin.sort_values(by=date_col, ascending=True)
    df_origin = df_origin[True - df_origin[y_col].isnull()]

    # if len(df_origin) == 0:
    #     print('函数 ExtractPointFromDf_DateX：删除空值后，dataframe为空！入参df中不含指定列')
    #     return df_origin

    # 提取时间，并将时间转为秒
    df_origin['seconds'] = df_origin.apply(lambda x: convert_time_str_to_second(str(x[date_col])[11:19]), axis=1)

    # 单独取出相应两列，准备转成point格式
    df_part = df_origin.loc[:, ['seconds', y_col]]

    # 将df转为array
    point_array = list(map(lambda x: (x[0], float(x[1])), df_part.values))

    return point_array


def addAcTemp(canvas_param, opc_df_today,pos_x, pos_y, width, height):

    total_df = opc_df_today

    #  取出
    # “室外天气”、
    # “冷却侧供水温度”、
    # “冷却侧回水温度”、
    # “冷冻侧供水温度”、
    # “冷冻侧回水温度”
    total_df_OAT = total_df[total_df.browse_name == 'OA-T']

    total_df_CSSWT = total_df[total_df.browse_name == 'CS-SWT']
    total_df_CSRWT = total_df[total_df.browse_name == 'CS-RWT']

    total_df_FSSWT = total_df[total_df.browse_name == 'FS-SWT']
    total_df_FSRWT = total_df[total_df.browse_name == 'FS-RWT']

    # 生成5个变量相应的点阵
    data_OAT = ExtractPointFromDf_DateX(df_origin=total_df_OAT, date_col='present_value_source_timestamp',
                                        y_col='present_value_value')

    data_CSSWT = ExtractPointFromDf_DateX(df_origin=total_df_CSSWT, date_col='present_value_source_timestamp',
                                          y_col='present_value_value')
    data_CSRWT = ExtractPointFromDf_DateX(df_origin=total_df_CSRWT, date_col='present_value_source_timestamp',
                                          y_col='present_value_value')

    data_FSSWT = ExtractPointFromDf_DateX(df_origin=total_df_FSSWT, date_col='present_value_source_timestamp',
                                          y_col='present_value_value')
    data_FSRWT = ExtractPointFromDf_DateX(df_origin=total_df_FSRWT, date_col='present_value_source_timestamp',
                                          y_col='present_value_value')

    data_origin = [tuple(data_OAT), tuple(data_CSSWT), tuple(data_CSRWT), tuple(data_FSSWT), tuple(data_FSRWT)]

    # 定义各曲线标签
    data_name_origin = ['室外温度', '冷却侧供水温度', '冷却侧回水温度', '冷冻侧供水温度', '冷冻侧回水温度']

    # 处理某条线没有数据的情况，若不处理“没有数据”的情况，画线的时候会报错！
    data = []
    data_name = []

    for i in range(0, len(data_origin)):
        if len(data_origin[i]) != 0:
            data.append(data_origin[i])
            data_name.append(data_name_origin[i])

    if len(data) == 0:
        print('函数 addAcTemp：原始df解析后没有想要的温度数据！')
        return canvas_param

    c = canvas_param
    # c.setFont("song", 10)

    drawing = Drawing(width=width, height=height)

    lp = LinePlot()
    # lp.x = 50
    # lp.y = 50
    lp.height = height
    lp.width = width
    lp.data = data
    lp.joinedLines = 1

    # 定义各曲线颜色
    lp.lines[0].strokeColor = colors.blue
    lp.lines[1].strokeColor = colors.red
    lp.lines[2].strokeColor = colors.lightgreen
    lp.lines[3].strokeColor = colors.orange
    lp.lines[4].strokeColor = colors.darkgreen

    for i in range(0, len(data)):
        lp.lines[i].name = data_name[i]
        lp.lines[i].symbol = makeMarker('FilledCircle', size=0.5)
        lp.lines[i].strokeWidth = 0.2

    # lp.lineLabelFormat = '%2.0f'
    # lp.strokeColor = colors.black

    lp.xValueAxis.valueMin = 0
    lp.xValueAxis.valueMax = 60*60*24
    lp.xValueAxis.valueSteps = [n for n in range(0, 60*60*24, 60*60)]
    lp.xValueAxis.labelTextFormat = lambda x: str(s2t(x))[0:2]
    lp.yValueAxis.valueMin = 0
    # lp.yValueAxis.valueMax = 50
    # lp.yValueAxis.valueSteps = [1, 2, 3, 5, 6]
    drawing.add(lp)
    add_legend(draw_obj=drawing, chart=lp, pos_x=10, pos_y=-10)

    try:
        renderPDF.draw(drawing=drawing, canvas=c, x=pos_x, y=pos_y)
    except:
        print('')
    return c

def addMultVoltPageToPdf(canvas_param,
                         volt_list,
                         col_name,
                         maxAmount=8,
                         minPercent=0.01,
                         pos_x=10,
                         pos_y=letter[1]*0.5,
                         width=letter[0]*0.8,
                         height=letter[1]*0.4):

    """
    函数功能：
                增加多表对比显示页，用于对多只表组合的系统的一个全面展示

    :param canvas_param:        画布
    :param volt_list:           表的list
    :param col_name:
    :return:
    """

    # 从多表中整理数据，前提为：volt的today字段中已经添加了原始的数据
    # （重要！today中添加的应该是该设备当天的原始数据，即完全从数据库）
    volt_list_pro = []

    # 删除没有df中没有数据的表
    volt_list_filter = list(filter(lambda x: not x.today.empty, volt_list))

    if len(volt_list_filter) == 0:
        canvas_param.drawString(x=10, y=letter[1] - 100, text='本页所列电表皆没有数据！')
        canvas_param.showPage()
        return canvas_param

    # 从电表列表的原始数据中整理提取每天数据
    for v in volt_list_filter:

        # 如果该dk的数据包含多个表地址，则根据表地址二次筛选
        if 'channel' in v.today.columns:
            if len(v.today.groupby(by='channel')) > 1:
                df_today_f = v.today[v.df_today.channel == v.meter_address]
            else:
                df_today_f = v.today
        else:
            df_today_f = v.today

        # 将‘data’列中的数据提取
        df_today_f = ExtractJsonToColum(df_today_f, 'data')

        # 删除数据中record_code 为2的行
        if 'record_type' in df_today_f.columns:
            df_today_f = df_today_f[True - df_today_f.record_type.isin(['2'])]

        v.add_today_data(df_today_f)

        # 将当天数据添加到电表对象中
        volt_list_pro.append(v)

    # 对电表进行数量约束，不重要的电表归总在虚拟电表“其他”中
    volt_list_pro = moveVoltToOthers(volt_list_pro, maxAmount=maxAmount, minPercent=minPercent, colName=col_name)

    # 提取各个电表的df
    # volt_df_today_list = list(map(lambda x: x.today, volt_list_pro))

    # 数据合并
    (values, percent, note_list) = concatVolt(voltDfList=volt_list_pro, col_name=col_name)

    # 画柱状图并添加到画布中
    voltGroupDisplayByBar(canvas_param=canvas_param,
                          df=values,
                          note_list=note_list,
                          pos_x=pos_x,
                          pos_y=pos_y,
                          width=width,
                          height=height)

    # 结束当前页,不宜在函数中结束当前页的编辑，因为其他函数也可能会编辑本页！
    # canvas_param.showPage()

    return canvas_param

