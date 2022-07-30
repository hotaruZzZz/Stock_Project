import pymysql


# 連結 SQL
connect_db = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='stock', charset='utf8')

'''
#建立table
with connect_db.cursor() as cursor:
    sql = """
    CREATE TABLE IF NOT EXISTS Data(
        ID int NOT NULL AUTO_INCREMENT PRIMARY KEY,
        StockName varchar(20),
        StockCode varchar(10),
        SDate datetime,
        Transactions float(50),
        StockHihg float(50),
        StockLow  float(50),
        StockOpen float(50),
        StockClose float(50)
        );
    """
    
    # 執行 SQL 指令
    cursor.execute(sql)
    # 提交至 SQL
    connect_db.commit()
'''

#新增資料
with connect_db.cursor() as cursor:
    sql = """
    INSERT INTO Data (StockName, StockCode, SDate, Transactions, StockHihg, StockLow, StockOpen, StockClose) VALUES 
    ('長榮', '2603', '2022-07-30', 57416, 96.80, 93.80, 93.90, 95.50)
    """
    
    # 執行 SQL 指令
    cursor.execute(sql)
    
    # 提交至 SQL
    connect_db.commit()
    
#查詢資料
with connect_db.cursor() as cursor:
    sql = """
    SELECT * from Data
    """
    
    # 執行 SQL 指令
    cursor.execute(sql)
    
    # 取出全部資料
    data = cursor.fetchall()
    print(data)    
    
    
    
# 關閉 SQL 連線
connect_db.close()