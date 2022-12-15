#import numpy as np
#import talib
#import os
#import requests
#from io import StringIO
#import pandas as pd
from pandas import DataFrame
import numpy as np
#import time
import pymysql
#from datetime import datetime, timedelta
list_id = []
suggest_list = np.zeros((0,0))
for i in range(10):         #range(10)改成list_id
    #資料庫連線設定
    #可縮寫db = pymysql.connect("localhost","root","root","30days" )
    db = pymysql.connect(host='localhost', port=3306, user='test', passwd='1234123zxc', db='django', charset='utf8')
    data = []
    #建立操作游標
    cursor = db.cursor()
    #SQL語法
    sql = (
        "select * from stock_data_data where sDate > '2022-11-01' and sNumber = '"
        + i +
        "' and sClose != (-1.00);"
        )#執行語法
    try:
      cursor.execute(sql)
      result = DataFrame(cursor.fetchall())
      data = result
      #提交修改
      db.commit()
      print('success')
    except:
      #發生錯誤時停止執行SQL
      db.rollback()
      print('error')
      
    #關閉連線
    db.close()
  
    #data = ["1.2","5""8.7","33","3.5","5","23"]
    print(data)#close = np.array(data)
    close = data[7]
    list_id = []
    import studen_suggest
    suggest , number = studen_suggest.suggest_stude(data, len(data))
    if suggest:
        suggest_list = np.append(suggest , np.array([[i , number]]) , axis = 0)
max_number = 0
for i in range(len(suggest)):
    if max_number < suggest_list[i][1]:
        max_number = suggest_list[i][1]

print("suggest:\n" , suggest_list)
print('best suggest: ' , max_number)