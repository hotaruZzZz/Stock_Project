import requests
from io import StringIO
import pandas as pd
import numpy as np

#查詢每日資訊
#輸入日期
date = input('Enter date(ex:20180131): ')
datestr = date

# 下載股價
r = requests.post('https://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date=' + datestr + '&type=ALL')

# 整理資料，變成表格
df = pd.read_csv(StringIO(r.text.replace("=", "")), 
            header=["證券代號" in l for l in r.text.split("\n")].index(True)-1)

#dataframe 轉換成 list
code = list(df['證券代號'])
n = input('輸入證券代號: ')

#查詢資料
for i in range(len(df)-1): 
    if(n == code[i]):
        print(df.loc[i])
        break

