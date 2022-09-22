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
       
def studen_start_linear(X, y):      #進行資料訓練，並且儲存
    import matplotlib.pyplot as plt
    from keras.models import Sequential
    from keras.layers import Dense, Activation, Dropout
    from keras.optimizers import SGD#, Adam
    #import numpy as np
    n = 10 #10項式
    #資料標準化
    max_features, min_features = max(X), min(X)
    X = (X-min_features)/(max_features-min_features)
    max_labels, min_labels = max(y), min(y)
    y = (y-min_labels)/(max_labels-min_labels)
    #資料多項式處理化
    from sklearn.preprocessing import PolynomialFeatures
    poly_features = PolynomialFeatures(degree = n, include_bias=False)
    X_expanded = poly_features.fit_transform(X)
    
    train_X = X_expanded
    train_y = y
    '''
    #分割資料比例 => test_size = %
    from sklearn.model_selection import train_test_split
    test_X, train_X = train_test_split(X_expanded, test_size=0.2, random_state=42) 
    test_y, train_y = train_test_split(y, test_size=0.2, random_state=42) 
    '''
    #神經網路
    model = Sequential()
    model.add(Dense(20, input_dim=n))
    model.add(Dropout(0.2)) # Dropout 20%
    model.add(Dense(10, input_dim=10))
    model.add(Dropout(0.2)) # Dropout 20%
    model.add(Dense(1, input_dim=2))
    model.add(Activation('linear'))
    
    
    #mse => mean_squared_error
    #adam = Adam(lr=1e-3)
    model.compile(loss='mse',optimizer=SGD(0.05))
    #, validation_split=0.2
    model.fit(train_X, train_y, epochs=200, batch_size=len(X), verbose=0)
    model.save("studen_deep_linear.h5")
    '''
    #學習曲線
    from sklearn.metrics import mean_squared_error
    from sklearn.model_selection import train_test_split
    def plot_learning_curves(model, X, y):
        X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=10)
        train_errors, val_errors = [], []
        for a in range(1, len(X_train) + 1):
            model.fit(X_train[:a], y_train[:a], epochs=20, batch_size=200, verbose=0)
            y_train_predict = model.predict(X_train[:a])
            y_val_predict = model.predict(X_val)
            train_errors.append(mean_squared_error(y_train[:a], y_train_predict))
            val_errors.append(mean_squared_error(y_val, y_val_predict))
        plt.plot(np.sqrt(train_errors), "r-+", linewidth=2, label="train")
        plt.plot(np.sqrt(val_errors), "b-", linewidth=3, label="val")
        plt.legend(loc="upper right", fontsize=14) # not shown in the book
        plt.xlabel("Training set size", fontsize=14) # not shown
        plt.ylabel("RMSE", fontsize=14) 
    
    plot_learning_curves(model, X_expanded, y)
    plt.axis([0, 80, 0, 3])
    plt.show()
    '''
    #分析
    pred = model.predict(train_X) 
    X = X * (max_features-min_features) + min_features
    y = y * (max_labels-min_labels) + min_labels
    pred = pred * (max_labels-min_labels) + min_labels
    plt.plot(X, y, "b--o", label = 'data')
    plt.plot(X, pred, "r-^", label = 'linear') 
    plt.legend(loc="best", fontsize=14)
    plt.show()

def studen_start_use(X , y):    #使用現有訓練模型
    import matplotlib.pyplot as plt
    from keras.models import load_model
    #from keras.layers import Dense, Activation, Dropout
    #from keras.optimizers import SGD, Adam
    n = 10 #10項式
    #資料標準化
    max_features, min_features = max(X), min(X)
    X = (X-min_features)/(max_features-min_features)
    max_labels, min_labels = max(y), min(y)
    y = (y-min_labels)/(max_labels-min_labels)
    #資料多項式處理化
    from sklearn.preprocessing import PolynomialFeatures
    poly_features = PolynomialFeatures(degree = n, include_bias=False)
    X_expanded = poly_features.fit_transform(X)
    #模型
    model = load_model("studen_deep_linear.h5")
    #分析
    pred = model.predict(X_expanded) 
    X = X * (max_features-min_features) + min_features
    y = y * (max_labels-min_labels) + min_labels
    pred = pred * (max_labels-min_labels) + min_labels
    plt.plot(X, y, "b--o", label = 'data')
    plt.plot(X, pred, "r-^", label = 'linear') 
    plt.legend(loc="best", fontsize=14)
    plt.show()
    
def studen_bollinger_bands(X , y , n_days): # 布林通道計算
    import numpy as np
    bollinger_bands = [] #布林通道
    SD = [] #標準差
    total = 0
    SD_total = 0
    for i in range(n_days-1, n_days*2-1):
        for j in range(i , i-5 , -1):
            total = y[j] + total
            SD_total = y[j]*y[j] + SD_total
        avg = total/n_days # 平均
        bollinger_bands.append(avg)
        SD.append((SD_total/n_days - avg * avg) ** (1/2))   #公式 sqrt(平方總和/n - 平均^2)
        total = 0
        SD_total = 0
    np_bollinger_bands = np.array(bollinger_bands).reshape(n_days,1)
    np_SD = np.array(SD).reshape(n_days, 1)  
    up_bollinger_bands = np_bollinger_bands + 2*np_SD
    dn_bollinger_bands = np_bollinger_bands - 2*np_SD
    studen_start_use(y , up_bollinger_bands)
    studen_start_use(y , dn_bollinger_bands)
    studen_start_use(y , np_bollinger_bands)

def studen_deep_suggest(X, y , n_days):
    import matplotlib.pyplot as plt
    from keras.models import load_model
    import numpy as np
    #from keras.layers import Dense, Activation, Dropout
    #from keras.optimizers import SGD, Adam
    n = 10 #10項式
    suggest = np.zeros((5,1))
    for i in range(n_days):
        suggest[i][0] = X[i][0] + 1
    #資料標準化
    max_features, min_features = max(suggest), min(suggest)
    suggest = (suggest-min_features)/(max_features-min_features)
    max_labels, min_labels = max(y), min(y)
    y = (y-min_labels)/(max_labels-min_labels)
    #資料多項式處理化
    from sklearn.preprocessing import PolynomialFeatures
    poly_features = PolynomialFeatures(degree = n, include_bias=False)
    X_expanded = poly_features.fit_transform(suggest)
    #模型
    model = load_model("studen_deep_linear.h5")
    #分析
    pred = model.predict(X_expanded) 
    suggest = suggest * (max_features-min_features) + min_features
    y = y * (max_labels-min_labels) + min_labels
    pred = pred * (max_labels-min_labels) + min_labels
    plt.plot(X, y, "b--o", label = 'data')
    plt.plot(suggest, pred, "r-^", label = 'linear') 
    plt.legend(loc="best", fontsize=14)
    plt.show()