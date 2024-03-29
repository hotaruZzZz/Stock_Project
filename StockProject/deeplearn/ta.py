import numpy as np
from pandas import DataFrame
import pymysql


#資料庫連線設定
#可縮寫db = pymysql.connect("localhost","root","root","30days" )
db = pymysql.connect(host='localhost', port=3306, user='test', passwd='1234123zxc', db='django', charset='utf8')
data = []
#建立操作游標
cursor = db.cursor()
#SQL語法
sql = "select * from stock_data_data where sDate > '2022-11-01' and sNumber = '00' and sClose != (-1.00);"
#執行語法
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

