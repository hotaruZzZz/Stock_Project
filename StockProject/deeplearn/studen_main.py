import studen_requests
import studen_deep_linear
import numpy as np

#輸入要查詢天數
#n_days = int(input('Enter days: '))
n_days = 10
data , D , date= studen_requests.get_data(n_days)   #給予資料、日期、天數
close = studen_requests.get_close(data)             #給予收盤價
Open = studen_requests.get_Open(data)               #給予開盤價
high = studen_requests.get_high(data)               #給予最高價
low = studen_requests.get_low(data)                 #給予最低價
volume = studen_requests.get_volume(data)           #給予成交股數
PE = studen_requests.get_PE(data)                   #給予本益比
name = studen_requests.get_name(data,volume)        #給予公司名稱
#輸入股票代號
#code = input('輸入股票代號: ')
code = '2330'
#將上面全部資料挑出輸入股票代號資料
X_close , X_high , X_low , X_Open = studen_requests.get_code(
    date, close , Open, low, high , name , D, n_days , code)
y_date = []

#把日期轉換為數字，例如:2022-8-19 => 8*31+19 = 267
for i in range(n_days):
    total = studen_deep_linear.Date_converts_list(D[i]) + D[i].day 
    y_date.append(total)
print(X_close, '\n'
     ,X_high , '\n'
     ,X_low  , '\n'
     ,X_Open , '\n')
#輸入需觀看資料類別
while True:
    look = input("觀看哪種資料(close/Open/high/low):")
    if look == 'close' or look == 'Open' or look == 'high' or look == 'low':
        break
    print("並無此資料種類，請重新輸入。")
#將需觀看類別資料轉換為numpy資料列
if look == 'close':
    X_X = np.array(X_close).reshape(n_days, 1)
    Y_Y = np.array(y_date).reshape(n_days, 1)
elif look == 'Open':
    X_X = np.array(X_Open).reshape(n_days, 1)
    Y_Y = np.array(y_date).reshape(n_days, 1)
elif look == 'high':
    X_X = np.array(X_high).reshape(n_days, 1)
    Y_Y = np.array(y_date).reshape(n_days, 1)
elif look == 'low':
    X_X = np.array(X_low).reshape(n_days, 1)
    Y_Y = np.array(y_date).reshape(n_days, 1)

Use = input("訓練(Y)或預測(N):")
if Use == 'y' or Use == 'Y':
    studen_deep_linear.studen_start_linear(Y_Y , X_X)   #進行訓練模式
elif Use == 'n' or Use == 'N':
    studen_deep_linear.studen_start_use(Y_Y , X_X)      #讀取已有模型
    #計算準確率(待完成)
else:
    print("ERROR")
