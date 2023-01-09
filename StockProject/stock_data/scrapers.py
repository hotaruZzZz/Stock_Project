from abc import ABC, abstractmethod
from datetime import datetime
from io import StringIO
import datetime
import time
import pandas as pd
import numpy as np
import requests

# 票券網站抽象類別
class Website(ABC):
 
    def __init__(self, stock_number):
        self.stock_number = stock_number  
        
    @abstractmethod
    def scrape(self):  # 爬取票抽象方法
        pass
    @abstractmethod
    def scrape_day(self):
        pass


def crawl_price(date):
    r = requests.post('http://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date=' + str(date).split(' ')[0].replace('-','') + '&type=ALL')
    ret = pd.read_csv(StringIO("\n".join([i.translate({ord(c): None for c in ' '}) 
                                    for i in r.text.split('\n') 
                                    if len(i.split('",')) == 17 and i[0] != '='])), header=0)
    ret = ret.set_index('證券代號')
    ret['成交金額'] = ret['成交金額'].str.replace(',','')
    ret['成交股數'] = ret['成交股數'].str.replace(',','')
    return ret

class TWSE(Website): #台灣證券交易所


    
    

    def scrape(self):
        
        data = {}
        if self.stock_number: #如果非空直
            #輸入要查詢天數
            n_days = int(7)
            date = datetime.datetime.now()
            D = []
            fail_count = 0
            allow_continuous_fail_count = 5

            while len(data) < n_days:
                try:
                    # 抓資料
                    data[date.date()] = crawl_price(date)
                    #print('success!')
                    fail_count = 0
                    D.append(date.strftime('%Y/%m/%d'))
                except:
                    # 假日爬不到
                    fail_count += 1
                    if fail_count == allow_continuous_fail_count:
                        raise
                        break
                # 減一天
                date -= datetime.timedelta(days=1)

            #收盤價
            close = pd.DataFrame({k:d['收盤價'] for k,d in data.items()}).transpose()
            close.index = pd.to_datetime(close.index)
            #開盤價
            open = pd.DataFrame({k:d['開盤價'] for k,d in data.items()}).transpose()
            open.index = pd.to_datetime(open.index)
            #最高價
            high = pd.DataFrame({k:d['最高價'] for k,d in data.items()}).transpose()
            high.index = pd.to_datetime(high.index)
            #最低價
            low = pd.DataFrame({k:d['最低價'] for k,d in data.items()}).transpose()
            low.index = pd.to_datetime(low.index)
            #成交股數
            volume = pd.DataFrame({k:d['成交股數'] for k,d in data.items()}).transpose()
            #本益比
            PE = pd.DataFrame({k:d['本益比'] for k,d in data.items()}).transpose()
            PE.index = pd.to_datetime(PE.index)
            volume.index = pd.to_datetime(volume.index)
            name = pd.DataFrame({k:d['證券名稱'] for k,d in data.items()}).transpose()
            name.index = pd.to_datetime(name.index)


      
            DD = np.array(D)
     
            SO = list(open[self.stock_number]['2022'].dropna().astype(float).values)
            SC = list(close[self.stock_number]['2022'].dropna().astype(float).values)
            SL = list(low[self.stock_number]['2022'].dropna().astype(float).values)
            SH = list(high[self.stock_number]['2022'].dropna().astype(float).values)
            result = []
            result.append(dict(sname=name[self.stock_number][0],snumber=self.stock_number))
            for i in range(n_days):
                d = DD[i]
                o = SO[i]
                h = SH[i]
                l = SL[i]
                c = SC[i]
                result.append(dict(day=d,sopen=o,shigh=h,slow=l,sclose=c))
            
            return result

    def scrape_day(self):

        data = {}
        if 1 == 1: #如果非空直
            #輸入要查詢天數
            n_days = int(1)
            #self.day = 1
            date = datetime.datetime.now()
            D = []
            fail_count = 0
            allow_continuous_fail_count = 5

            while len(data) < n_days:
                try:
                    # 抓資料
                    data[date.date()] = crawl_price(date)
                    #print('success!')
                    fail_count = 0
                    D.append(date.strftime('%Y/%m/%d'))
                except:
                    # 假日爬不到
                    fail_count += 1
                    if fail_count == allow_continuous_fail_count:
                        raise
                        break
                # 減一天
                date -= datetime.timedelta(days=1)
            # 收盤價
            close = pd.DataFrame({k: d['收盤價'] for k, d in data.items()}).transpose()

            # 開盤價
            open = pd.DataFrame({k: d['開盤價'] for k, d in data.items()}).transpose()

            # 最高價
            high = pd.DataFrame({k: d['最高價'] for k, d in data.items()}).transpose()

            # 最低價
            low = pd.DataFrame({k: d['最低價'] for k, d in data.items()}).transpose()

            # 成交股數
            volume = pd.DataFrame({k: d['成交股數'] for k, d in data.items()}).transpose()
            # 本益比
            PE = pd.DataFrame({k: d['本益比'] for k, d in data.items()}).transpose()

            name = pd.DataFrame({k: d['證券名稱'] for k, d in data.items()}).transpose()

            stock = {
                'name': name,
                'close': close,
                'open': open,
                'high': high,
                'low': low,
                'volume': volume,
            }
            result = []
            for i in stock['name'].keys():
                #N.append(stock['name'][i].values)
                if(stock['open'][i].values[0] == '--'):#若沒有值則設為-1
                    stock['open'][i].values[0] = str(-1)
                    stock['high'][i].values[0] = str(-1)
                    stock['low'][i].values[0] = str(-1)
                    stock['close'][i].values[0] = str(-1)
                    stock['volume'][i].values[0] = str(-1)
                #print(stock['name'][i].values[0] + ' ' + stock['open'][i].values[0] + ' ' + stock['close'][i].values[0])
                result.append(dict(sday=stock['name'].index.values[0],index=i,sname=stock['name'][i].values[0],sopen=stock['open'][i].values[0].replace(',',''),shigh=stock['high'][i].values[0].replace(',',''),
                                   slow=stock['low'][i].values[0].replace(',',''),sclose=stock['close'][i].values[0].replace(',',''),svolume=stock['volume'][i].values[0].replace(',','')))
           
     
            
            return result