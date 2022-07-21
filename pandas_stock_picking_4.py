import requests
from io import StringIO
import pandas as pd
import numpy as np


#查詢每日資訊
#輸入日期
date = input('Enter date(ex:20180131): ')
datestr = date
data = {}
try:#抓資料
    # 下載股價
    r = requests.post('https://www.twse.com.tw/exchangeReport/BWIBBU_d?response=csv&date=' + datestr + '&type=ALL')
    
    ret = pd.read_csv(StringIO("\n".join([i.translate({ord(c): None for c in ' '}) 
                                        for i in r.text.split('\n') 
                                        if len(i.split('",')) == 8 and i[0] != '='])), header=0)
    ret = ret.set_index('證券代號')
   #輸入證券代號
    code = int(input('輸入證券代號: '))
    data[code] = ret 
    #股價淨值比
    PBR = pd.DataFrame({k:d['股價淨值比'] for k,d in data.items()}).transpose()
    #殖利率(%)
    Yield = pd.DataFrame({k:d['殖利率(%)'] for k,d in data.items()}).transpose()
    #本益比
    PE = pd.DataFrame({k:d['本益比'] for k,d in data.items()}).transpose()

    stock = {'PBR':PBR[code],'Yield':Yield[code],'PE':PE[code]}

    print('股價淨值比:' , stock['PBR'].values)
    print('殖利率(%):' , stock['Yield'].values)
    print('本益比:' , stock['PE'].values)

except:
        # 假日爬不到
        print('fail! check the date is holiday')



