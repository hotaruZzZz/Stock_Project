import requests
from io import StringIO
import pandas as pd
import numpy as np

def get_data(n_days):

    def crawl_price(date):
        r = requests.post('http://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date=' + str(date).split(' ')[0].replace('-','') + '&type=ALL')
        ret = pd.read_csv(StringIO("\n".join([i.translate({ord(c): None for c in ' '}) 
                                            for i in r.text.split('\n') 
                                            if len(i.split('",')) == 17 and i[0] != '='])), header=0)
        ret = ret.set_index('證券代號')
        ret['成交金額'] = ret['成交金額'].str.replace(',','')
        ret['成交股數'] = ret['成交股數'].str.replace(',','')
        return ret
    
    import datetime
    import time
    
    data = {}

    date = datetime.datetime.now()
    D = []
    fail_count = 0
    allow_continuous_fail_count = 5
    # 開始測量
    start = time.time()
    
    while len(data) < n_days:
        
        print('parsing', date)
        # 使用 crawPrice 爬資料
        try:
            # 抓資料
            data[date.date()] = crawl_price(date)
            print('success!')
            fail_count = 0
            D.append(date.date())
        except:
            # 假日爬不到
            print('fail! check the date is holiday')
            fail_count += 1
            if fail_count == allow_continuous_fail_count:
                raise
                break
        
        # 減一天
        date -= datetime.timedelta(days=1)
        #time.sleep(10)
    
    # 結束測量
    end = time.time()
    print("執行時間：%f 秒" % (end - start))
    return data , D , date

def get_close(data):
    #收盤價
    close = pd.DataFrame({k:d['收盤價'] for k,d in data.items()}).transpose()
    close.index = pd.to_datetime(close.index)
    return close
def get_Open(data):
    #開盤價
    Open = pd.DataFrame({k:d['開盤價'] for k,d in data.items()}).transpose()
    Open.index = pd.to_datetime(Open.index)
    return Open
def get_high(data):
    #最高價
    high = pd.DataFrame({k:d['最高價'] for k,d in data.items()}).transpose()
    high.index = pd.to_datetime(high.index)
    return high
def get_low(data):
    #最低價
    low = pd.DataFrame({k:d['最低價'] for k,d in data.items()}).transpose()
    low.index = pd.to_datetime(low.index)
    return low
def get_volume(data):
    #成交股數
    volume = pd.DataFrame({k:d['成交股數'] for k,d in data.items()}).transpose()
    volume.index = pd.to_datetime(volume.index)
    return volume
def get_PE(data):
    #本益比
    PE = pd.DataFrame({k:d['本益比'] for k,d in data.items()}).transpose()
    PE.index = pd.to_datetime(PE.index)
    return PE
def get_name(data, volume):
    name = pd.DataFrame({k:d['證券名稱'] for k,d in data.items()}).transpose()
    name.index = pd.to_datetime(name.index)
    return name
def get_code(date, close , Open, low, high , name , D, n_days , code):
    #輸入年分
    year = str(date.year)
    #股票相關資料，轉成float 格式
    stock = {
        'open':Open[code]['2022'].dropna().astype(float),
        'close':close[code]['2022'].dropna().astype(float),
        'low':low[code]['2022'].dropna().astype(float),
        'high':high[code]['2022'].dropna().astype(float),
    }
    
    D = np.flipud(D)
    
    stock['open'] = np.flipud(stock['open'])
    stock['close'] = np.flipud(stock['close'])
    stock['low'] = np.flipud(stock['low'])
    stock['high'] = np.flipud(stock['high'])
    SO = list(np.flipud(Open[code]['2022'].dropna().astype(float).values))
    SC = list(np.flipud(close[code]['2022'].dropna().astype(float).values))
    SL = list(np.flipud(low[code]['2022'].dropna().astype(float).values))
    SH = list(np.flipud(high[code]['2022'].dropna().astype(float).values))
    DA = [SO,SC,SL,SH]
    DAA = np.transpose(np.array(DA)).tolist()
    #print(DAA)
    End_close = []
    End_high = []
    End_low = []
    End_Open = []
    print(name[code][0])
    for i in range(n_days):
        print(D[i], stock['open'][i],stock['high'][i],stock['low'][i],stock['close'][i])#日期 開盤 最高 最低 收盤
        End_close.append(stock['close'][i])
        End_high.append(stock['high'][i])
        End_low.append(stock['low'][i])
        End_Open.append(stock['open'][i])
    return End_close , End_high , End_low , End_Open