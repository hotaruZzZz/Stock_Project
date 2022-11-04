import studen_deep_linear
import numpy as np
import pandas as pd
from datetime import datetime

#pd.read_csv(data_name => 檔案名稱 ,usecols = [] => 選取指定列, nrows => 幾筆資料)
data = (pd.read_csv("tech_every_day3.csv")
        [lambda x: x['stock_id'] == 15 ]     #lambda x:x*x為密名函示 , 類似 def a(x): return x*x
        )
new_data = data[~(data['mean5'].isnull())]        #選取在mean5標籤下並非NaN值
mean5_data = new_data["mean5"]
time_data = new_data["date"]
n_days = len(new_data)
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
    y_date.insert(0,total)  
Y_Y = np.array(y_date).reshape(n_days , 1)
#Y_Y => 日期
#X_X => 當日往後五天平均
#開始訓練
model = studen_deep_linear.studen_start_linear(Y_Y , X_X)
XX , YY , ss , pp = studen_deep_linear.studen_deep_suggest(Y_Y , X_X , n_days)

n = 20
from sklearn.preprocessing import PolynomialFeatures
poly_features = PolynomialFeatures(degree = n, include_bias=False)
train_X_expanded = poly_features.fit_transform(np.arange(2000,2250).reshape(250,1))
num = 1
for i in model.predict(train_X_expanded):
    print(num, ":" , i)
    num+=1