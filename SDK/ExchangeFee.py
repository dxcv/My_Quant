# encoding=utf-8

"""

有关交易费用相关的函数

买进费用：
1、佣金：中信：0.00025 国信：0.001        不足5元按5元收取
2、过户费：仅限沪市，1000股  1元（已取消？）
3、通信费：（已取消？）


卖出费用：
1、佣金：中信：0.00025 国信：0.001        不足5元按5元收取
2、过户费：仅限沪市，1000股  1元 （已取消？）
3、印花税：0.001
4、通信费：（已取消？）

"""
import math

from General.GlobalSetting import g_total_stk_info_mysql
from SDK.StkSub import getNameByStkCode


def WhichMarketStkIn(stk_code):
    """
    判断是沪市还是深市
    :param stk_code:
    :return: sh，sz

            不识别的股票代码返回空字符串
    """

    if stk_code[0:2] == '60':
        return 'sh'

    elif stk_code[0:2] == '00' or stk_code[0:3] == '300':
        return 'sz'

    else:
        print('函数 WhichMarketStkIn：不识别的股票代码：'+stk_code)
        return ''


def calExchangeFee(stk_code, stk_amount, stk_price, buy=True, commissionRatio=0.00025, stampTaxRatio=0.001):
    """
    计算每笔交易的费用
    :param stk_code:
    :param stk_amount:
    :param stk_price:
    :return:
    """

    # 计算当前交易总价格
    price_total = stk_amount*stk_price

    site = WhichMarketStkIn(stk_code)

    if site == '':
        print('函数 calExchangeFee：无法识别stk所在交易所！')
        return -1

    # 过户费 上交所每1000股收费1元
    transferFee = math.ceil(stk_amount / 1000) * 1

    # 佣金
    commission = stk_amount * stk_price * commissionRatio

    if commission < 5:
        commission = 5

    # 印花税
    stampTax = stk_amount*stk_price*stampTaxRatio

    # -------------------------------------------- 买入时 ----------------------------------------
    if buy:
        if site=='sh':
            print('函数 calExchangeFee：'+'\n'+
                  '交易股票：'+getNameByStkCode(g_total_stk_info_mysql, stk_code)+'\n'+
                  '所在交易所：'+{'sh':'上交所','sz':'深交所'}.get(site)+'\n'+
                  '买入卖出：'+'买入'+'\n'+
                  '印花税：'+'无'+'\n'+
                  '过户费：'+str(transferFee)+'\n'+
                  '佣金：'+str(commission)+'\n'+
                  '费用总计：'+str(transferFee+commission)+'\n')

            # 沪市买入 佣金 + 过户费
            return transferFee+commission

        else:
            print('函数 calExchangeFee：'+'\n'+
                  '交易股票：'+getNameByStkCode(g_total_stk_info_mysql, stk_code)+'\n'+
                  '所在交易所：'+{'sh':'上交所','sz':'深交所'}.get(site)+'\n'+
                  '买入卖出：'+'买入'+'\n'+
                  '印花税：'+'无'+'\n'+
                  '过户费：'+'无'+'\n'+
                  '佣金：'+str(commission)+'\n'+
                  '费用总计：'+str(commission)+'\n')

            # 深市买入 佣金
            return commission

    # ------------------------------ 卖出时 ------------------------------------
    else:

        if site == 'sh':
            print('函数 calExchangeFee：' + '\n' +
                  '交易股票：' + getNameByStkCode(g_total_stk_info_mysql, stk_code) + '\n' +
                  '所在交易所：' + {'sh': '上交所', 'sz': '深交所'}.get(site) + '\n' +
                  '买入卖出：' + '卖出' + '\n' +
                  '印花税：' + str(stampTax) + '\n' +
                  '过户费：' + str(transferFee) + '\n' +
                  '佣金：' + str(commission) + '\n' +
                  '费用总计：' + str(transferFee + commission+stampTax) + '\n')

            # 沪市卖出 佣金 + 过户费+印花税
            return transferFee + commission

        else:
            print('函数 calExchangeFee：' + '\n' +
                  '交易股票：' + getNameByStkCode(g_total_stk_info_mysql, stk_code) + '\n' +
                  '所在交易所：' + {'sh': '上交所', 'sz': '深交所'}.get(site) + '\n' +
                  '买入卖出：' + '卖出' + '\n' +
                  '印花税：' + str(stampTax) + '\n' +
                  '过户费：' + '无' + '\n' +
                  '佣金：' + str(commission) + '\n' +
                  '费用总计：' + str(commission+stampTax) + '\n')

            # 深市卖出 佣金+印花税
            return commission+stampTax


""" ================================== 测试 ======================================= """
# calExchangeFee(stk_code='300183', stk_amount=400, stk_price=17.3, buy=False)