# encoding = utf-8

# ======================================== 创建画布信息 ====================================
from reportlab.pdfgen import canvas

from Auto_Report.ReportLab.SubFunction import *

c = canvas.Canvas("日度股票报告.pdf", pagesize=letter)
c.setFont("song", 10)
page_n = 1


# ========================================= 进行画图 ========================================

# 增加封面
c = addFront(canvas_param=c, theme='日度金融证券报告', subtitle='大中华民国一百零七年八月')

# 大盘
c.bookmarkPage("P" + str(page_n))
c.addOutlineEntry('上证', "P" + str(page_n), closed=1)
page_n += 1

c.showPage()
c.save()