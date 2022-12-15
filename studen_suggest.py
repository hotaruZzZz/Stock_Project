import studen_deep_linear
import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

def suggest_start(new_data , n_days):
    #pd.read_csv(data_name => 檔案名稱 ,usecols = [] => 選取指定列, nrows => 幾筆資料)
    #tech_every_day3裡面目前有1943個不同ID，想查詢的話請找另外製作的ID表
    
    mean5_data = new_data["mean5"]                    #"mean5"這個選項可以改成"open"
    time_data = new_data["date"]
    X_X = mean5_data.values
    np_time_data = time_data.values
    number_time_data = []
    y_date = []
    
    #將存在np_time_data裡面的字串時間轉換為datetime，以方便後續轉換數字
    for i in np_time_data:
        a = str(i)
        date = datetime.strptime(a , "%Y-%m-%d")
        number_time_data.append(date)
    #把日期轉換為數字，例如:2007-1-1 ~ 2020-8-31 => (2007-2007)*365+fun(1-1)+1 ~ (2020-2007)*365+fun(8-1)+31
    first_year = number_time_data[0].year
    for i in range(n_days):
        total = ((number_time_data[i].year-first_year)*365
               + studen_deep_linear.Date_converts_list(number_time_data[i]) 
               + number_time_data[i].day) 
        y_date.append(total)  
    Y_Y = np.array(y_date).reshape(n_days , 1)
    X_X = X_X.reshape(n_days , 1)
    #Y_Y => 日期
    #X_X => 當日往後五天平均
    
    #↑以上，為提取資料，如果模組沒問題的話只要動上半部
    #-------------------------------------------分隔線----------------------------------------------------------
    #↓以下，為訓練預測資料，大概只要改改參數就OK了
    
    #資料標準化
    max_features, min_features = max(X_X), min(X_X)
    X_X = (X_X-min_features)/(max_features-min_features)
    #資料三維處理
    n = 30 #幾天為一筆
    X_train = []
    y_train = []
    for i in range(n, n_days):
        X_train.append(X_X[i-n:i, 0])
        y_train.append(X_X[i, 0])
    X_train, y_train = np.array(X_train), np.array(y_train)
    X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
    
    #開始訓練
    model , pred = studen_deep_linear.studen_CNN_LSTM_model(
        X_train , y_train, epochs = 6 , batch_size = 20 , learning_rate = 0.001
        )
    X_pred , Y_pred = studen_deep_linear.studen_predict(X_X , Y_Y, n , days = 31)
    new_time_data = np_time_data
    for i in range(31):
        time_str = new_time_data[len(new_time_data)-1]
        da = int(time_str[8:])
        mo = int(time_str[5:7])
        Ya = int(time_str[:4])
        new_data = studen_deep_linear.create_data(Ya , mo , da)
        new_time_data = np.append(new_time_data, np.array([new_data]) , axis = 0)
    #轉化為原始檔
    X_X = X_X * (max_features-min_features) + min_features
    pred = pred * (max_features-min_features) + min_features
    X_pred = X_pred * (max_features-min_features) + min_features
    #繪製
    #draw_data(第一個X軸，第一個Y軸，第二個X軸，第二個Y軸，上下間距，範圍開啟(0為關閉，其他數字都是開啟)，標題)
    studen_deep_linear.draw_data(np_time_data , X_X, new_time_data, X_pred, n, axis = 1 , name = 'data_predict')
    studen_deep_linear.draw_data(np_time_data , X_X, np_time_data[n:] , pred, n, axis = 0 , name = 'data_learing')
    #draw_data_for_date(np_time_data , X_X , 30)
    #Y_pred[len(Y_pred)-n]+3
    if X_pred[len(X_pred)-1] <= X_X[len(X_X)-1]:
        suggest = 0
    else:
        suggest = 1
    if __name__ == "__main__":
        return suggest , X_pred , pred , np_time_data , X_X , Y_Y
    else:
        number = X_X[len(X_X)-1] - X_pred[len(X_pred)-1]
        return suggest , number
    
if __name__ == "__main__":
    data = (pd.read_csv("tech_every_day3.csv")
           [lambda x: x['stock_id'] == 6201 ]     #lambda x:x*x為密名函示 , 類似 def a(x): return x*x
            )
    new_data = data[~(data['mean5'].isnull())]        #選取在mean5標籤下並非NaN值
    n_days = len(new_data)  
    suggest , X_pred , pred , np_time_data , X_X , Y_Y = suggest_start(new_data , n_days)
    