# encoding = utf-8

# ======================================== 创建画布信息 ====================================
from reportlab.pdfgen import canvas

from Auto_Report.ReportLab.SubFunction import *

width = letter[0]
height = letter[1]

c = canvas.Canvas("day报告.pdf", pagesize=letter)
c.setFont("song", 10)
page_n = 1


# ========================================= 进行画图 ========================================

# 增加封面
c = addFront(canvas_param=c, theme='每日报告测试', subtitle='大中华民国一百零七年八月')

#
c.bookmarkPage("P" + str(page_n))
c.addOutlineEntry('上证', "P" + str(page_n), closed=1)
page_n += 1

# 具体画图
sh_index = ts.get_hist_data('cyb')
sh_index['date'] = sh_index.index
sh_index = sh_index.reset_index(drop=True)

# 按时间降序排序，方便计算macd
sh_index = sh_index.sort_values(by='date',ascending=True)

# 在原始df中增加macd信息
sh_index['MACD'],sh_index['MACDsignal'],sh_index['MACDhist'] = talib.MACD(sh_index.close,
                            fastperiod=12, slowperiod=26, signalperiod=9)

# 在原始数据中增加kdj信息
sh_index['slowk'], sh_index['slowd'] = talib.STOCH(sh_index.high,
                                                   sh_index.low,
                                                   sh_index.close,
                                                   fastk_period=9,
                                                   slowk_period=3,
                                                   slowk_matype=0,
                                                   slowd_period=3,
                                                   slowd_matype=0)

# 添加rsi信息
sh_index['RSI5'] = talib.RSI(sh_index.close, timeperiod=5)
sh_index['RSI12'] = talib.RSI(sh_index.close, timeperiod=12)
sh_index['RSI30'] = talib.RSI(sh_index.close, timeperiod=30)

sh_index = sh_index.dropna(axis=0,how='any')

close = ExtractPointFromDf_DateX(sh_index, 'date', 'close')
m5 = ExtractPointFromDf_DateX(sh_index, 'date', 'ma5')
m10 = ExtractPointFromDf_DateX(sh_index, 'date', 'ma10')
m20 = ExtractPointFromDf_DateX(sh_index, 'date', 'ma20')

macd = ExtractPointFromDf_DateX(sh_index, 'date', 'MACD')

data = [tuple(close),tuple(m5),tuple(m10),tuple(m20)]
data_name = ['close','m5','m10','m20']

drawing_ave = genLPDrawing(data=data, data_note=data_name)
renderPDF.draw(drawing=drawing_ave, canvas=c, x=10, y=height * 0.7)

drawing_macd = genBarDrawing(data=macd, data_note=['macd'])
renderPDF.draw(drawing=drawing_macd, canvas=c, x=10, y=height*0.5)



# 整理kdj信息
slowk = ExtractPointFromDf_DateX(sh_index, 'date', 'slowk')
slowd = ExtractPointFromDf_DateX(sh_index, 'date', 'slowd')
data_kdj = [tuple(slowk),tuple(slowd)]
data_kdj_note = ['k','d']

drawing_kdj = genLPDrawing(data=data_kdj, data_note=data_kdj_note,height=letter[1]*0.15)
renderPDF.draw(drawing=drawing_kdj, canvas=c, x=10, y=height * 0.35)

# 画图RSI信息




c.showPage()
c.save()