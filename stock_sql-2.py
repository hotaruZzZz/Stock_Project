import pymysql
import requests
from io import StringIO
import pandas as pd
import numpy as np

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

#輸入股票代號
code = input('輸入股票代號: ')
#股票相關資料，轉成float 格式
stock = {
    'name':name[code]['2022'],
    'close':close[code]['2022'].dropna().astype(float),
    'open':open[code]['2022'].dropna().astype(float),
    'high':high[code]['2022'].dropna().astype(float),
    'low':low[code]['2022'].dropna().astype(float),
    'volume': volume[code]['2022'].dropna().astype(float),
}


for i in range(n_days):
    print(D[i], stock['name'][i] , stock['volume'][i], stock['open'][i],stock['high'][i],stock['low'][i],stock['close'][i])



# 連結 SQL
connect_db = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='stock', charset='utf8')

#新增資料
with connect_db.cursor() as cursor:
    sql = "INSERT INTO Data (StockName, StockCode, SDate, Volumes, StockHihg, StockLow, StockOpen, StockClose) VALUES"
   
    for i in range(n_days):
        
        sql += "('" + str(stock['name'][i]) + "','" + str(code) + "','" + str(D[i]) + "'," + str(stock['volume'][i]) + "," + str(stock['high'][i])+","
        sql += str(stock['low'][i]) + ","+ str(stock['open'][i]) + "," + str(stock['close'][i]) + ")"
        if(i<n_days-1):
            sql+=","
        #print(D[i], stock['name'][i] , stock['volume'][i], stock['open'][i],stock['high'][i],stock['low'][i],stock['close'][i])
    
    
    # 執行 SQL 指令
    cursor.execute(sql)
    # 提交至 SQL
    connect_db.commit()

    
    
# 關閉 SQL 連線
connect_db.close()