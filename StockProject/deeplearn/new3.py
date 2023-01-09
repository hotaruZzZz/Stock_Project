from pandas import DataFrame
import numpy as np
import pymysql
import studen_suggest
#from deeplearn import studen_suggest

#from . import studen_suggest
#from datetime import datetime, timedelta
#資料庫連線設定
#可縮寫db = pymysql.connect("localhost","root","root","30days" )

db = pymysql.connect(host='localhost', port=3306, user='test', passwd='1234123zxc', db='django', charset='utf8')
cursor = db.cursor()
s = "select distinct(sNumber) from stock_data_data where sDate > '2022-11-01'  and sClose != (-1.00);"
list_id = []

try:
    cursor.execute(s)
    list_id = DataFrame(cursor.fetchall())
    db.commit()
    print('success')
except:
  #發生錯誤時停止執行SQL
  db.rollback()
  print('error')    
#關閉連線
db.close()

list_id = list_id.values
print(list_id)
print(type(list_id))
suggest_id = ['2603'
                ,'3034'
                ,'2454'
                ,'2382'
                ,'2357'
                ,'2409'
                ,'4938'
                ,'3711'
                ,'2324'
                ,'2347'
                ,'2301'
                ,'1102'
                ,'2303'
                ,'1402'
                ,'3231'
                ,'2356'
                ,'3702'
                ,'2891'
                ,'2379'
                ,'2377'
                ,'2027'
                ,'8046'
                ,'2890'
                ,'2317'
                ,'2885'
                ,'2474'
                ,'1301'
                ,'1303'
                ,'4958'
                ,'2376'
                ,'2385'
                ,'2337'
                ,'6239'
                ,'2383'
                ,'1802'
                ,'2915'
                ,'3036'
                ,'2542'
                ,'3044'
                ,'6176'
                ,'3189'
                ,'2637'
                ,'2449'
                ,'5522'
                ,'2606'
                ,'3017'
                ,'2006'
                ,'2809'
                ,'3665'
                ,'6271']
number_list = []
for i in suggest_id:         #range(10)改成list_id
    data = []

    db = pymysql.connect(host='localhost', port=3306, user='test', passwd='1234123zxc', db='django', charset='utf8')
    #建立操作游標
    cursor = db.cursor()
    #SQL語法
    sql = (
        "select * from stock_data_data where sDate > '2020-11-01' and sNumber = '"
        + str(i) +
        "' and sClose != (-1.00) order by sDate;"
        )#執行語法
    print(sql)
    try:
      cursor.execute(sql)
      result = DataFrame(cursor.fetchall())
      data = result
      if data.empty == True:
          #print('empty')
          pass
      else:
          #提交修改
          db.commit()
          #print(data)
          print('success')
    except:
      #發生錯誤時停止執行SQL
      db.rollback()
      print('error')
      
    #print(data)#close = np.array(data)
    #close = data[7]
    suggest , number, plotly, plotly_2 = studen_suggest.suggest_start(data, len(data) , 1)
    number_list.append((str(i) , number[0]))
#關閉連線
db.close()
max_number = 0
max_id = '0'
suggest_list = []
number_suggest = 0
for i in number_list:
    if max_number < i[1]:
        max_number = i[1]
        max_id = i[0]     
print("suggest:\n------" ,max_id,'------\n')