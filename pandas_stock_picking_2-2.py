import requests
from io import StringIO
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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
#輸入要查詢天數
n_days = int(input('Enter days: '))
date = datetime.datetime.now()
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

#輸入股票代號
code = input('輸入股票代號: ')
#輸入年分
year = str(date.year)
#股票相關資料，轉成float 格式
stock = {
    'close':close[code][year].dropna().astype(float),
    'open':open[code][year].dropna().astype(float),
    'high':high[code][year].dropna().astype(float),
    'low':low[code][year].dropna().astype(float),
    'volume': volume[code][year].dropna().astype(float),
    'PE': PE[code][year].dropna().astype(float),
}

#印出收盤價圖表

c, = plt.plot(stock['close'],label='close')
o, = plt.plot(stock['open'],label='open')
plt.legend(handles=[c,o], loc='best')
#plt.plot(stock['high'])
#plt.plot(stock['low'])
plt.xticks(rotation=45)
plt.title(code,fontproperties="SimSun")
plt.show()



