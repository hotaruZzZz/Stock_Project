import pymysql
#月營收
import pandas as pd
import requests
from io import StringIO
import time

def monthly_report(year, month):
    
    # 假如是西元，轉成民國
    if year > 1990:
        year -= 1911
    
    url = 'https://mops.twse.com.tw/nas/t21/sii/t21sc03_'+str(year)+'_'+str(month)+'_0.html'
    if year <= 98:
        url = 'https://mops.twse.com.tw/nas/t21/sii/t21sc03_'+str(year)+'_'+str(month)+'.html'
    
    # 偽瀏覽器
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    
    # 下載該年月的網站，並用pandas轉換成 dataframe
    r = requests.get(url, headers=headers)
    r.encoding = 'big5'

    dfs = pd.read_html(StringIO(r.text), encoding='big-5')

    df = pd.concat([df for df in dfs if df.shape[1] <= 11 and df.shape[1] > 5])
    
    if 'levels' in dir(df.columns):
        df.columns = df.columns.get_level_values(1)
    else:
        df = df[list(range(0,10))]
        column_index = df.index[(df[0] == '公司代號')][0]
        df.columns = df.iloc[column_index]
    
    df['當月營收'] = pd.to_numeric(df['當月營收'], 'coerce')
    df = df[~df['當月營收'].isnull()]
    df = df[df['公司代號'] != '合計']
    
    # 偽停頓
    time.sleep(5)

    return df

def Scrapying(y,m):
    #資料庫連線設定
    #可縮寫db = pymysql.connect("localhost","root","root","30days" )
    db = pymysql.connect(host='localhost', port=3306, user='test', passwd='1234123zxc', db='django', charset='utf8')
    #建立操作游標
    cursor = db.cursor()
    #年分與月份
    data = monthly_report(y,m) 

    for i,j in data.iterrows():
        code  =str(j['公司代號'])
        name = str(j['公司名稱'])
        year =  str(y)
        month = str(m)
        month_revenue = str(j['當月營收'])
        month_lastrevenue = str(j['上月營收'])
        month_lastyear = str(j['去年當月營收'])
        month_lastmol = str(j['上月比較增減(%)'])
        month_samemol = str(j['去年同月增減(%)'])
        month_grand = str(j['當月累計營收'])
        month_lastgrand = str(j['去年累計營收'])
        month_forwardmol = str(j['前期比較增減(%)'])
        #SQL語法
        sql = "INSERT INTO stock_data_monthlyrevenue values ( null,'"+ code + "','"  + name + "','"+ year + "','"+ month+"'," + month_lastrevenue + "," + month_lastyear + "," + month_lastmol + "," + month_samemol + "," + month_grand + ","  +  month_lastgrand + "," + month_forwardmol + "," + month_revenue +  ");"
        #print(sql)
        #執行語法
        try:
          cursor.execute(sql)
          #提交修改
          db.commit()
          print('success')
        except:
          #發生錯誤時停止執行SQL
          db.rollback()
          print('error')

    #關閉連線
    db.close()

    #輸出：success


#Scrapying(111, 11)

s = input('enter start year:')
e = input('enter end year:')
for i in range(int(s),int(e)+1):
     for j in range(1,13):
         Scrapying(i, j)
         