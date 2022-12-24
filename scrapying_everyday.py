import pymysql
import requests
from io import StringIO
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time



def crawl_price(date):
    r = requests.post('http://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date=' + str(date).split(' ')[0].replace('-','') + '&type=ALL')
    ret = pd.read_csv(StringIO("\n".join([i.translate({ord(c): None for c in ' '}) 
                                        for i in r.text.split('\n') 
                                        if len(i.split('",')) == 17 and i[0] != '='])), header=0)
    ret = ret.set_index('證券代號')
    ret['成交金額'] = ret['成交金額'].str.replace(',','')
    ret['成交股數'] = ret['成交股數'].str.replace(',','')
    # 偽停頓
    #time.sleep(5)
    return ret


def scraping(date):
    data = []
    # 使用 crawPrice 爬資料
    try:
        # 抓資料
        data = crawl_price(date)
        print(date+'success!')
        #print(data)
        return data
    except:
        # 假日爬不到
        print('fail! check the date is holiday')
        return 0

def DB(start,end):
    
    db = pymysql.connect(host='localhost', port=3306, user='test', passwd='1234123zxc', db='django', charset='utf8')
    #建立操作游標
    cursor = db.cursor()
   
    s = start
    d = datetime.strptime(s, '%Y%m%d')
    while(s < end):
        
        data = scraping(s)
        #print(data)
        #rint(type((scraping(s))))
        if(str(type(data))=="<class 'int'>"):
            
            d = datetime.strptime(s, '%Y%m%d')
            d  = d + timedelta(days=1)
            s = d.strftime('%Y%m%d')
            
        else:
            
            for i,j in data.iterrows():
                #print(s)
                #print(type(data))
                sName = j['證券名稱']
                sNumber = i
                sDate = s
                sOpen = j['開盤價'] if j['開盤價'] != '--' else (-1)
                sHigh = j['最高價'] if j['最高價'] != '--' else (-1)
                sLow = j['最低價'] if j['最低價'] != '--' else (-1)
                sClose = j['收盤價'] if j['收盤價'] != '--' else (-1)
                sChange = j['漲跌價差'] if j['漲跌價差'] != '--' else (-1)
                sDir = j['漲跌(+/-)'] 
                sLastBestAskPrice = j['最後揭示賣價'] if j['最後揭示賣價'] != '--' else (-1)
                sLastBestAskVolume = j['最後揭示賣量'] if j['最後揭示賣量'] != '--' else (-1)
                sLastBestBidPrice = j['最後揭示買價'] if j['最後揭示買價'] != '--' else (-1)
                sLastBestBidVolume = j['最後揭示買量'] if j['最後揭示買量'] != '--' else (-1)
                sPE = j['本益比'] if j['本益比'] != '--' else (-1)
                sTradeValue = j['成交金額'] if j['成交金額'] != '--' else (-1)
                sTradeVolume = j['成交股數'] if j['成交股數'] != '--' else (-1)
                sTransaction = j['成交筆數'] if j['成交筆數'] != '--' else (-1)
                sql = "insert into  stock_data_data value ( null, '" + sName + "', '" + str(sNumber) + "', '" + str(sDate) + "',"  + str(sOpen).replace(',','') + "," + str(sHigh).replace(',','') + "," + str(sLow).replace(',','') + "," + str(sClose).replace(',','') + "," + str(sChange).replace(',','') + ",'" + str(sDir) + "'," + str(sLastBestAskPrice).replace(',','') + "," + str(sLastBestAskVolume).replace(',','') + "," + str(sLastBestBidPrice).replace(',','') + "," + str(sLastBestBidVolume).replace(',','') + "," + str(sPE).replace(',','') + "," + str(sTradeValue).replace(',','') +"," + str(sTradeVolume).replace(',','') + "," + str(sTransaction).replace(',','') + ");"
                #print(sql)
                
                
                #sql = ""
                #執行語法
                
                try:
                  cursor.execute(sql)
                  #提交修改
                  db.commit()
                  print('success')
                  
                except:
                  #發生錯誤時停止執行SQL
                  db.rollback()
                  print(sql)
                  print('error')
                  break
            d = datetime.strptime(s, '%Y%m%d')
            d  = d + timedelta(days=1)
            s = d.strftime('%Y%m%d')  
            
            
                
    #關閉連線
    db.close()       

start = input('Enter start date: ')
end = input('Enter end date: ')
DB(start,end)
#print(scraping(start))
#scraping(start, end)
