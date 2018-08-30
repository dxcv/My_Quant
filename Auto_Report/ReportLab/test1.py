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
c = addFront(canvas_param=c, theme='日度金融证券报告', subtitle='大中华民国一百零七年八月')

#
c.bookmarkPage("P" + str(page_n))
c.addOutlineEntry('上证', "P" + str(page_n), closed=1)
page_n += 1

# 具体画图
sh_index = ts.get_hist_data('cyb')
sh_index['date'] = sh_index.index
sh_index = sh_index.reset_index(drop=True)

close = ExtractPointFromDf_DateX(sh_index, 'date', 'close')
m5 = ExtractPointFromDf_DateX(sh_index, 'date', 'ma5')
m10 = ExtractPointFromDf_DateX(sh_index, 'date', 'ma10')
m20 = ExtractPointFromDf_DateX(sh_index, 'date', 'ma20')

data = [tuple(close),tuple(m5),tuple(m10),tuple(m20)]
data_name = ['close','m5','m10','m20']

drawing = Drawing(width=width*0.8, height=height*0.4)

lp = LinePlot()
# lp.x = 50
# lp.y = 50
lp.height = height*0.4
lp.width = width*0.8
lp.data = data
lp.joinedLines = 1

# 定义各曲线颜色
lp.lines[0].strokeColor = colors.blue
lp.lines[1].strokeColor = colors.red
lp.lines[2].strokeColor = colors.lightgreen
lp.lines[3].strokeColor = colors.orange
# lp.lines[4].strokeColor = colors.darkgreen

for i in range(0, len(data)):
    lp.lines[i].name = data_name[i]
    lp.lines[i].symbol = makeMarker('FilledCircle', size=0.5)
    lp.lines[i].strokeWidth = 0.2

# lp.lineLabelFormat = '%2.0f'
# lp.strokeColor = colors.black

x_min = data[0][0][0]
x_max = data[0][-1][0]

lp.xValueAxis.valueMin = x_min
lp.xValueAxis.valueMax = x_max

step = int(((x_max - x_min)/(60*60*24))/30) + 1

lp.xValueAxis.valueSteps = [n for n in range(int(x_min), int(x_max), 60*60*24*step)]
lp.xValueAxis.labelTextFormat = lambda x: str(Sec2Datetime(x)[0:10])
lp.xValueAxis.labels.angle = 90
lp.xValueAxis.labels.dy = 5
# lp.yValueAxis.valueMin = 90
# lp.yValueAxis.valueMax = 50
# lp.yValueAxis.valueSteps = [1, 2, 3, 5, 6]
drawing.add(lp)
add_legend(draw_obj=drawing, chart=lp, pos_x=10, pos_y=-10)

renderPDF.draw(drawing=drawing, canvas=c, x=10, y=height*0.4)

c.showPage()
c.save()