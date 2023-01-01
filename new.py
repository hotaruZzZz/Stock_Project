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
import random
suggest_id = []
a = 0
for i in range(20):
    random_number = random.randrange(22748)
    for j in suggest_id:
        if j == random_number:
            a = 1
            break
    if a == 0:
        print(random_number)
        suggest_id.append(list_id[random_number])
    else:
        a = 0
first = ['0050']
suggest_id.insert(0 , np.array(first))
for i in suggest_id:
    print(i[0])
def fun(db , cursor , suggest_id):
    b = 0
    first_number = 0
    number_list = []
    for i in suggest_id:         #range(10)改成list_id
        data = []
    
        db = pymysql.connect(host='localhost', port=3306, user='test', passwd='1234123zxc', db='django', charset='utf8')
        #建立操作游標
        cursor = db.cursor()
        #SQL語法
        sql = (
            "select * from stock_data_data where sDate > '2020-11-01' and sNumber = '"
            + str(i[0]) +
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
        if b == 0:
            first_number = studen_suggest.suggest_start(data, len(data) , b)
            b = 1
        else:
            suggest , number, plotly, plotly_2 = studen_suggest.suggest_start(data, len(data) , b)
            number_list.append((str(i[0]) , number[0]))
    #關閉連線
    db.close()
    return first_number[0], number_list
suggest_list = []
BREAK = 1
total = 1
while BREAK:
    if len(suggest_list) == 0:
        first_number , number_list = fun(db , cursor , suggest_id)
        number_suggest = 0
        
        print(type(first_number) , first_number)
        print('-----------%d sugggest---------------'%total)
        total += 1
        for i in number_list:
            #print(type(i[0]) , i[0])
            if first_number < i[1]:
                suggest_list.append(i[0])
    else:
        print("suggest:\n" , suggest_list)
        BREAK = 0
