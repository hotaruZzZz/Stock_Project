from pandas import DataFrame
import numpy as np
import pymysql
import studen_suggest

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


suggest_list = np.zeros((1,2))

list_id = list_id.values
#print(list_id)

data = []
db = pymysql.connect(host='localhost', port=3306, user='test', passwd='1234123zxc', db='django', charset='utf8')
#建立操作游標
cursor = db.cursor()
#SQL語法
sql = (
    "select * from stock_data_data where sDate > '2020-11-01' and sNumber = '"
    + code +
    "' and sClose != (-1.00);"
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
      
#關閉連線
db.close()
    
print(data)#close = np.array(data)
close = data[10]
list_id = []
    
suggest , number = studen_suggest.suggest_start(data, len(data))
print(suggest , number)
print('-----------return ---------------')
if suggest:
    suggest_list = np.append(suggest_list , np.array([[a , number[0]]]) , axis = 0)
    print('---------end---------------')
max_number = 0
number_suggest = 0
print('-------sugggest---------------')
for i in range(len(suggest_list)):
    if max_number < suggest_list[i][1]:
        max_number = suggest_list[i][1]
        number_suggest = i

print("suggest:\n" , suggest_list[1:])
print('best suggest: ' , number_suggest)
