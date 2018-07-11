# -*- coding: utf-8 -*-
"""
@author: GuoJun
"""

from WindPy import w
import logging as log
from pandas import DataFrame, Series
import datetime, time
from datetime import timedelta, datetime
import os
from dateutil.relativedelta import relativedelta
from ConnectDB import connDB, connClose, get_data, get_all_data

# BASE_DIR = os.path.dirname(__file__)
# LOG_PATH = BASE_DIR +'/log/data_update/'
# LOG_FILENAME = 'CIGRG_001_' + str(time.strftime('%Y%m%d_%H%M%S',time.localtime(time.time()))) + '.log'
log.basicConfig(
    # filename = LOG_PATH + LOG_FILENAME,
    level=log.DEBUG,
    # format="[%(asctime)s] %(name)s:%(levelname)s: %(message)s"
    format="%(levelname)s: %(message)s")
#############################
# 常量设置
PE = 30
PB = 3
ROE = 12
DIVIDEND_RATE = 0.01
WEIGHT = 0.95
MKT_CAP = 5000000000
TOP_STOCK_NUMBER = 10

# requestDate = '2012-03-27'
#############################
w.start()
# 获取中证红利回报（H30073.CSI）和中证红利（000922.SH）成分股，以及全部A股
# set_date = 'date=' + requestDate
# divSet1 = w.wset('sectorconstituent', set_date,'windcode=H30073.CSI;field=wind_code').Data[0]
# divSet2 = w.wset('sectorconstituent', set_date,'windcode=000922.SH;field=wind_code').Data[0]
# divSet3 = w.wset('sectorconstituent', set_date, 'sectorid=a001010100000000;field=wind_code').Data[0]
# 合并去重
# divSet = list(set(divSet1 + divSet2 + divSet3))
# divSet = w.wset('sectorconstituent', set_date, 'sectorid=a001010100000000').Data[1]

items = 'symbol, ipo'
table = 'stk_info'
condition = ' where area not in (\'黑龙江\',\'吉林\',\'辽宁\')'
ipo_data = get_all_data(items, table, condition)

def stock_list(requestDate):
    divSet= []
    # IPO日期过滤掉上市时间低于3年的公司
    # setValue_ipo = w.wsd(divSet, "ipo_date", requestDate, requestDate, "TradingCalendar=SZSE")
    set_ipo_remove = []
    for a in range(0, len(ipo_data)):
        divSet.append(ipo_data[a][0])
        if ipo_data[a][1] >= datetime.date(datetime.strptime(requestDate, '%Y-%m-%d') - relativedelta(years=3)):
            set_ipo_remove.append(ipo_data[a][0])
    divSet = list(set(divSet).difference(set(set_ipo_remove)))

    # 过滤掉总市值低于特定值公司，排除小市值公司策略的干扰
    items = 'symbol, mktcap'
    table = 'stk_price'
    condition = ' where date = \'' + requestDate + '\' and symbol in (' + str(divSet).replace('[','').replace(']','') + ') order by symbol'
    mkt_data = get_all_data(items, table, condition)
    set_marketCap_remove = []

    # setValue_marketCap = w.wsd(divSet, "mkt_cap_ashare2", requestDate, requestDate,"unit=1;currencyType=;TradingCalendar=SZSE")
    for b in range(0, len(mkt_data)):
        if mkt_data[b][1] <= MKT_CAP:
            set_marketCap_remove.append(mkt_data[b][0])
    divSet = list(set(divSet).difference(set(set_marketCap_remove)))

    # 过滤掉非正常状态的公司

    # PE值过滤
    setValue_pe = w.wsd(divSet, "pe_ttm", requestDate, requestDate, "TradingCalendar=SZSE;Fill=Previous").Data[0]
    set_pe_remove = []
    for i in range(0, len(setValue_pe)):
        if setValue_pe[i] >= PE or setValue_pe[i] <= 0:
            set_pe_remove.append(divSet[i])
    divSet = list(set(divSet).difference(set(set_pe_remove)))

    # PB值过滤
    setValue_pb = w.wsd(divSet, "pb_lf", requestDate, requestDate, "TradingCalendar=SZSE;Fill=Previous").Data[0]
    set_pb_remove = []
    for j in range(0, len(setValue_pb)):
        if setValue_pb[j] >= PB or setValue_pb[j] <= 0:
            set_pb_remove.append(divSet[j])
    divSet = list(set(divSet).difference(set(set_pb_remove)))

    # 股息收益率要大于5年国债收益率
    setValue_dividendyield = \
    w.wsd(divSet, "dividendyield2", requestDate, requestDate, "TradingCalendar=SZSE;Fill=Previous").Data[0]
    set_dividendyield_remove = []
    for k in range(0, len(setValue_dividendyield)):
        if setValue_dividendyield[k] <= DIVIDEND_RATE:
            set_dividendyield_remove.append(divSet[k])
    divSet = list(set(divSet).difference(set(set_dividendyield_remove)))

    # 三年平均ROE过滤与排序
    setValue_roe_reportDate = w.wsd(divSet, "latelyrd_bt", requestDate, requestDate,
                                    "Period=Q;Days=Alldays;Fill=Previous")  # 获取有效报表日期，避免未来数据
    set_roe_value_avg = []
    set_roe_remove = []
    set_roe = {}
    for d in range(0, len(divSet)):
        setValue_roe = w.wsd(divSet, "roe_ttm2", setValue_roe_reportDate.Data[0][d] - relativedelta(years=3), setValue_roe_reportDate.Data[0][d], "Period=Q;Days=Alldays")
        try:
            setValue_roe.Data[d] = [x for x in setValue_roe.Data[d] if str(x) != 'nan']
        except Exception as e:
            log.info(e)

        if len(setValue_roe.Data[d]) < 7:
            set_roe_remove.append(divSet[d])
            continue

        e_avg_temp = 1  # 计算三年ROE指数平均值
        for roe_q in setValue_roe.Data[d]:
            e_avg_temp = e_avg_temp * (1 + roe_q / 100)

        if e_avg_temp <= 1:  # 三年ROE指数平均值低于1直接淘汰
            set_roe_remove.append(divSet[d])
            continue
        set_roe_value_avg.append(100 * (e_avg_temp ** (1 / len(setValue_roe.Data[d])) - 1))
        set_roe[divSet[d]] = set_roe_value_avg[-1]

        if set_roe_value_avg[-1] <= ROE or setValue_roe.Data[d][-1] <= ROE:  # 三年ROE指数均值或最后一期ROE低于低于标准者剔除
            set_roe_remove.append(divSet[d])
            del set_roe[divSet[d]]

    divSet = list(set(divSet).difference(set(set_roe_remove)))

    if len(divSet) > 1:
        set_roe_order = sorted(set_roe.items(), key=lambda d: d[1], reverse=True)

        ##  排序
        # 股息率排序
        set_div = {}
        set_div_value = w.wsd(divSet, "dividendyield2", requestDate, requestDate, "Period=Q;Days=Alldays;Fill=Previous")
        for t in range(0, len(set_div_value.Data[0])):
            set_div[set_div_value.Codes[t]] = set_div_value.Data[0][t]
        set_div_order = sorted(set_div.items(), key=lambda d: d[1], reverse=True)

        # ROE与股息率综合排名
        set_order = {}
        for x in range(0, len(divSet)):
            set_order[divSet[x]] = set_roe_order[x][1] * WEIGHT + set_div_order[x][1] * (1 - WEIGHT)
        set_order_stock = sorted(set_order.items(), key=lambda d: d[1], reverse=True)

        order_list = []
        for stock in set_order_stock:
            order_list.append(stock[0])

        if len(order_list) > 10:
            order_list = order_list[:TOP_STOCK_NUMBER]

    elif len(divSet) == 1:
        order_list = divSet

    else:
        order_list = []

    return order_list
# #
# list = stock_list('2012-05-09')
# log.info(list)
