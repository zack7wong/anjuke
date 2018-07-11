import pandas as pd
import numpy as np
from WindPy import w
import datetime, time
import statsmodels.api as sm
from statsmodels import regression
import matplotlib.pyplot as plt
from copy import deepcopy


pd.set_option('expand_frame_repr', False)
w.start()

#设定无风险利率
rf = 0.04
asset = 1000000 #起始资金100万

#设定调仓频率
T = 50
S = 63 #样本长度
N = 10 #一次买入10只股票

end_date = datetime.datetime.today().strftime('%Y%m%d')
start_date=w.tdaysoffset(-872, end_date, "").Times[0]

#沪深300加上创业板成分股做股票池
hsCodes = w.wset('indexconstituent', 'date=' + str(start_date) + ';windcode=000016.SH')
# Codes = w.wset("sectorconstituent", 'date=' + str(start_date) + ";windcode=399006.SZ")

code_list = hsCodes.Data[1]

winddate=w.tdays(start_date,end_date, "")
tradedate= [i.strftime('%Y%m%d') for i in winddate.Times]

holding = {}

# #剔除st股的全部股票做股票池
# stockCodes = w.wset("sectorconstituent", "date=" + str(start_date) + ";sectorid=a001010100000000;field=wind_code")
# code_list = stockCodes.Data[0]
# stcode = w.wset("carryoutspecialtreatment", 'startdate' + str(start_date) + ';enddate=2018-03-16')
# code_list = [i for i in code_list if i not in stcode.Data[0]]


#选股函数
def stock_add(date,codelist):

    # 获得样本期间的股票价格并计算日收益率
    r_date = w.tdaysoffset(-63, date, "").Times[0]
    price_df = pd.DataFrame()
    feasible_stocks = []
    for code in codelist:
        price_wd = w.wsd(code, "close,trade_status", r_date,date)
        pricelist = price_wd.Data[0]
        if all([s == '交易' for s in price_wd.Data[1]]):
            price_chg = np.diff(np.log(pricelist),axis=0)
            price_df[code]= price_chg
            feasible_stocks.append(code)

    sdata = pd.DataFrame()
    removelist = []
    for code in feasible_stocks:
        tradestatus = w.wsd(code, "trade_status", "ED-0TD",date)
        if tradestatus.Data[0][0] == '交易':
            wdata = w.wsd(code, "windcode,close,val_pe_deducted_ttm,eps_ttm,ev3,equity_new", "ED-0TD",date, "gRateType=1;unit=1;currencyType=;Fill=Previous;PriceAdj=F")
            df = pd.DataFrame(wdata.Data, index=['股票代码','收盘价','EPSL','EPS', '总市值', '股东权益'],
                              columns=wdata.Times).T
            df['PE'] = df['收盘价']/df['EPS']
            df['G'] = (df['EPS']-df['EPSL'])*100/df['EPSL']
            df['PEG'] = df['PE']/df['G']
            #账面市值比就是账面的所有者权益除以市值（下以简称B/M）。
            df['BTM'] = df['股东权益']/df['总市值']
            sdata = sdata.append(df)
        else:
            removelist.append(code)

    feasible_stocks = [i for i in feasible_stocks if i not in removelist]

    #去掉无用的列
    sdata = sdata[['股票代码','收盘价','总市值','PEG','BTM']]
    sdata = sdata.dropna()


    #选出特征股票组合
    length = len(sdata)
    SF = sdata.sort_values('总市值')['股票代码'][:int(length/3)]
    SA = sdata.sort_values('总市值')['股票代码'][int(length - length/3):]
    LF = sdata.sort_values('BTM')['股票代码'][:int(length/3)]
    LA = sdata.sort_values('BTM')['股票代码'][int(length - length/3):]

    S = np.sum(price_df[SF].T) / len(SF) - np.sum(price_df[SA].T) / len(SA)
    L = np.sum(price_df[LA].T) / len(LA) - np.sum(price_df[LF].T) / len(LF)

    #以上证指数作为基准
    index_wd = w.wsd('000001.SH', "close", r_date, date, "gRateType=1;unit=1;currencyType=;Fill=Previous;PriceAdj=F")
    indexlist = index_wd.Data[0]
    RM = np.diff(np.log(indexlist)) - rf/252
#
    #将三因子放在一张表里
    X = pd.DataFrame({'RM': RM, 'S': S, 'L': L })
    factor_flag = ['RM', 'S', 'L']
    X = X[factor_flag]

    #对样本回归计算alpha值
    t_scores = [0.0] * length
    for i in range(length):
        t_stock = feasible_stocks[i]
        price_change = (price_df[t_stock] - rf / 252)
        t_r = linreg(X, price_change, len(factor_flag))
        t_scores[i] = t_r[0]

    #打分列表
    scores = pd.DataFrame({'code':feasible_stocks,'score':t_scores})
    scores = scores.sort_values('score').head(10)

    # #选出彼得林奇的好股票
    # sdata = sdata[(sdata['PEG']>0)&(sdata['PEG']<1)]
    return list(scores['code'])

#输入:X:回归自变量 Y:回归因变量
def linreg(X, Y, columns=3):
    X = sm.add_constant(np.array(X))
    Y = np.array(Y)
    if len(Y) > 1:
        results = regression.linear_model.OLS(Y, X).fit()
        return results.params
    else:
        return [float("nan")] * (columns + 1)


def mock_trading(tradedate,codelist):
    asset = 1000000
    # 历史持仓表
    holding = {}

    for i in range(0,len(tradedate),T):
        Dtime = deepcopy(tradedate[i])
        buy_list = stock_add(tradedate[i],codelist)
        print(Dtime)
        if len(holding) == 0:
            close_list = w.wss(buy_list, "close", "tradeDate="+ tradedate[i] +";priceAdj=U;cycle=D").Data[0]
            amount = asset/len(buy_list)/(np.array(close_list))
            holding[Dtime] = [buy_list,list(amount),close_list]
            print('开仓持有的股票是{}'.format(holding[tradedate[i]][0]))

        else:

            # date_index = list(holding.keys())[-1]
            preholding = deepcopy(holding[tradedate[i-T]])
            sell_list = []
            sell_list_amount = []
            sell_hold_price = []
            del_index = []
            for index, code in enumerate(preholding[0]):
                if code not in buy_list:
                    sell_list.append(code)
                    sell_list_amount.append(preholding[1][index])
                    sell_hold_price.append(preholding[2][index])
                    del_index.append(index)
            for i in range(len(del_index)):
                preholding[0].pop(del_index[i] - i)
                preholding[1].pop(del_index[i] - i)
                preholding[2].pop(del_index[i] - i)
            if len(sell_list) == 0:
                continue
            sell_close_list  = w.wss(sell_list, "close","tradeDate="+ Dtime +";priceAdj=U;cycle=D").Data[0]
            if len(sell_close_list)>0:
                profit = sum((np.array(sell_close_list) - np.array(sell_hold_price))*np.array(sell_list_amount))
            else:
                profit = 0
            asset = asset + profit
            print('卖出股票是{}'.format(sell_list))
            print('股票盈亏是{}'.format(profit))

            buy_list = [i for i in buy_list if i not in preholding[0]]
            buy_close_list = w.wss(buy_list, "close", "tradeDate="+ Dtime +";priceAdj=U;cycle=D").Data[0]
            amount = asset / len(buy_list) / np.array(buy_close_list)
            holding[Dtime] = [buy_list+preholding[0],list(amount)+preholding[1],buy_close_list+preholding[2]]
            print('买入的股票是{}'.format(buy_list))
            print('{}持仓是{}'.format(Dtime,holding[Dtime][0]))
            print('总资产是{}元'.format(asset))
            


if __name__ == '__main__':
    mock_trading(tradedate, code_list)
