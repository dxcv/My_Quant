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
renderPDF.draw(drawing=drawing_macd, canvas=c, x=10, y=height*0.55)


c.showPage()
c.save()