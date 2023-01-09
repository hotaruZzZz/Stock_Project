def year4(Year):    #判斷當年有無多一天
    fir = Year % 4
    sec = Year % 100
    thr = Year % 400
    if fir != 0:
        return 0
    if fir == 0 and sec != 0:
        return 1
    if sec == 0 and thr != 0:
        return 0
    if thr == 0:
        return 1

def Date_converts_list(D):  #轉換年月日為第幾天
    Year4 = year4(D.year)
    #判斷當月總日期
    total = 0
    Month = D.month
    for i in range(1, Month):
        if i == 1:
            total += 31
        elif i == 2:
            if Year4 == 1:
                total += 29
            else:
                total += 28
        elif i == 3:
            total += 31
        elif i == 4:
            total += 30
        elif i == 5:
            total += 31
        elif i == 6:
            total += 30
        elif i == 7:
            total += 31
        elif i == 8:
            total += 31
        elif i == 9:
            total += 30
        elif i == 10:
            total += 31
        elif i == 11:
            total += 30
        elif i == 12:
            total += 31
    return total

def create_data(year , month , day):
    nex = 30
    for i in [1,3,5,7,8,10,12]:
        if i == month:
            nex = 31 
            break
    if month == 2:
        if year4(year):
            nex = 29
        else:
            nex = 28
    if day+1 <= nex:
        day = day + 1
    else:
        day = 1
        if month+1 <= 12:
            month = month + 1
        else:
            month = 1
            year = year + 1
    for i in [1,2,3,4,5,6,7,8,9]:
        if i == month:
            month = '0'+ str(month)
            break
    return str(year) + '-' + str(month) + '-' + str(day)

def draw_plotly(X , y , new_X , new_Y , first_X, first_Y , n = 0 , axis = 0 , name = 'learing'):
    import plotly.express as px
    import plotly.graph_objects as go
    import plotly.io as pio
    from plotly.offline import plot
    print(len(X) ,":", len(y) ,":", len(new_X) ,":", len(new_Y) ,":" , len(first_X) ,":", len(first_Y), '\n')
    pio.renderers.default = 'browser' #這行是列應到瀏覽器上，加上上面那行事都是針對spyder做處理的，可斟酌註解
    list_y = y.tolist()
    list_new_x = new_X.tolist()
    list_new_y = new_Y.tolist()
    list_first_y = first_Y.tolist()
    print_x = X.tolist()
    print_y = []
    print_new_X = new_X.tolist()
    print_new_Y = []
    print_first_y = []
    for i in range(len(X)):
        print_y.append(list_y[i][0])
    for i in range(len(new_X)):
        print_new_Y.append(list_new_y[i][0])
    for i in range(len(first_X)):
        print_first_y.append(list_first_y[i][0])
    fig1 = go.Scatter(x=print_x, y=print_y, mode = "lines", name='data')
    fig2 = go.Scatter(x=print_new_X, y=print_new_Y, mode = "lines", name='learing',opacity=0.6)
    fig3 = go.Scatter(x=print_new_X, y=print_first_y, mode = "lines", name='0056')
    layout = go.Layout(title=name,yaxis_title='Close',)
    plot_div= plot({"data": [fig1,fig2,fig3],"layout": layout},output_type='div')
    return  plot_div
    #return print_x , print_y , print_new_X , print_new_Y, plot_div
    

def draw_data(X , y , new_X , new_Y , n = 0 , axis = 0 , name = 'learing'):
    import matplotlib.pyplot as plt
    import matplotlib.ticker as ticker
    ticker_spacing = 7 #len(X)/13  # 日期的字符串數組
    fig, ax = plt.subplots()
    range_1 = n
    range_2 = n+n+1
    if axis == 0:
        range_1 = len(X)
        range_2 = len(new_X)
        ticker_spacing = 365 #len(X)/13  # 日期的字符串數組
    plt.plot(X[len(X)-range_1:], y[len(X)-range_1:], "b--", label = 'data')
    plt.plot(new_X[len(new_X)-range_2:], new_Y[len(new_X)-range_2:], "r-", label = 'learing')
    plt.legend(loc="best", fontsize=14)
    plt.title(name, fontsize=18)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(ticker_spacing))
    plt.xticks(rotation=30)
    
    #plt.show()

def studen_CNN_LSTM_model(X, y , epochs = 5 , batch_size = 15 , learning_rate = 0.005):#進行資料訓練，並且儲存
    from keras.models import Sequential
    from keras.layers import Dense, LSTM , Dropout
    from keras.optimizers import Adam
    #神經網路
    model = Sequential()
    model.add(LSTM(units=50,input_shape = (X.shape[1], 1),return_sequences = True))#輸入層
    model.add(LSTM(units=50,return_sequences = True))
    model.add(LSTM(units=50,return_sequences = True,activation='linear'))
    model.add(Dropout(0.2))
    model.add(LSTM(units=50,activation='linear'))
    model.add(Dropout(0.2))
    model.add(Dense(units=16,kernel_initializer="uniform",activation='linear'))
    model.add(Dense(units=8,kernel_initializer="uniform",activation='linear'))
    model.add(Dense(units=4,kernel_initializer="uniform",activation='linear'))
    model.add(Dense(units=1))#最後輸出層
    #模型編譯，損失函示(Mean Squared Error)，優化契adam
    model.compile(loss='mse',optimizer=Adam(learning_rate = learning_rate))
    output = model.fit(X, y, epochs=epochs, batch_size=batch_size, validation_split=0.1, verbose=2)
    model.save("studen_deep_linear.h5")
    
    
    #分析
    pred = model.predict(X)
    return model , pred

def studen_predict(X, y, days = 14 , n_days = 30): #使用模型做預測做推薦
    from keras.models import load_model
    import numpy as np
    model = load_model("studen_deep_linear.h5")
    #N個資料為一筆資料訓練隔天的數據，一天一天往前推算數值
    for i in range(days):
        predict_data = X[len(X)-n_days:]
        train_array = predict_data
        train_array = np.reshape(train_array, (predict_data.shape[1], predict_data.shape[0], 1))
        new_pred = model.predict(train_array)
        X = np.append(X , new_pred , axis = 0)
    l = y[len(y)-1]
    for i in range(days):
        y = np.append(y, np.array([l+i+1]) , axis = 0)
    return X , y

def loss_function(X , y , n):
    max_features, min_features = max(X), min(X)
    X = (X-min_features)/(max_features-min_features)
    new_X , new_Y = studen_predict(X[:len(X)-n], y[:len(y)-n], days = n)
    X = X * (max_features-min_features) + min_features
    new_X = new_X * (max_features-min_features) + min_features
    draw_data(y, X, new_Y, new_X, n, axis = 1 , name = "valid")
    