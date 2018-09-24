# encoding = utf-8

from General.GlobalSetting import *
from SDK.SDKHeader import *

"""
    三次样条拟合测试
"""

# def cubic(a,b,c,d,x):
#     return a + b*x + c*x*x + d*x*x*x
#
#
# input = range(0,1000)
#
#
# y = list(map(lambda x:cubic(1,2,3,4,x),input))


import matplotlib.pyplot as plt
import numpy as np



x = np.arange(1,6)
y = np.array([1, 2, 3, 3.5, 3.8])

z1 = np.polyfit(x, y, 2)                                        #用3次多项式拟合
p1 = np.poly1d(z1)
print(p1)                                                       #在屏幕上打印拟合多项式

yvals = p1(x)                                                   #也可以使用yvals=np.polyval(z1,x)

plot1 = plt.plot(x, y, '*',label='original values')
plot2 = plt.plot(x, yvals, 'r',label='polyfit values')


