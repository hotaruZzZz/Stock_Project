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
   
def studen_learning_curve(model , X , y):   #學習曲線
    import numpy as np
    import matplotlib.pyplot as plt
    from sklearn.metrics import mean_squared_error
    from sklearn.model_selection import train_test_split
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=10)
    train_errors, val_errors = [], []
    for a in range(1, len(X_train) + 1):
        model.fit(X_train[:a], y_train[:a])
        #model.fit(X_train[:a], y_train[:a], epochs=20, batch_size=200, verbose=0)
        y_train_predict = model.predict(X_train[:a])
        y_val_predict = model.predict(X_val)
        train_errors.append(mean_squared_error(y_train[:a], y_train_predict))
        val_errors.append(mean_squared_error(y_val, y_val_predict))
    plt.plot(np.sqrt(train_errors), "r-+", linewidth=2, label="train")
    plt.plot(np.sqrt(val_errors), "b-", linewidth=3, label="val")
    plt.legend(loc="upper right", fontsize=14) # not shown in the book
    plt.xlabel("Training set size", fontsize=14) # not shown
    plt.ylabel("RMSE", fontsize=14) 
    plt.axis([0, 80, 0, 3])
    plt.show()

def draw_data(X , y , new_X , new_Y):
    import matplotlib.pyplot as plt
    plt.plot(X, y, "b--", label = 'data')
    plt.plot(new_X, new_Y, "r-", label = 'linear')
    plt.legend(loc="best", fontsize=14)
    plt.title("start_linear", fontsize=18)
    #plt.axis([2000, 2300, -100, 100])
    plt.show()

def studen_start_linear(X, y):      #進行資料訓練，並且儲存
    from keras.models import Sequential
    from keras.layers import Dense, Activation, Dropout
    from keras.optimizers import SGD#, Adam
    from sklearn.linear_model import LinearRegression

    n = 20 #10項式
    #資料標準化
    max_features, min_features = max(X), min(X)
    X = (X-min_features)/(max_features-min_features)
    max_labels, min_labels = max(y), min(y)
    y = (y-min_labels)/(max_labels-min_labels)
    #分割資料比例 => test_size = %
    size = 0.7
    from sklearn.model_selection import train_test_split
    test_X, train_X = train_test_split(X, test_size = size, random_state=42) 
    test_y, train_y = train_test_split(y, test_size = size, random_state=42) 
    #資料多項式處理化
    from sklearn.preprocessing import PolynomialFeatures
    poly_features = PolynomialFeatures(degree = n, include_bias=False)
    train_X_expanded = poly_features.fit_transform(train_X)
    #test_X_expanded = poly_features.fit_transform(test_X)
    X_expanded = poly_features.fit_transform(X)
    #train_X_expanded = train_X
    '''
    #神經網路
    model = Sequential()
    model.add(Dense(units=10,input_dim=n,activation='relu'))#輸入一維，輸出10，啟用函式relu/tanh
    model.add(Dropout(0.2))
    model.add(Dense(units=10,input_dim=10,activation='relu'))#輸入一維，輸出10，啟用函式relu/tanh
    model.add(Dense(units=1))#預設上一步輸入為10
    #模型編譯，損失函示(Mean Squared Logarithmic Error)，
    model.compile(loss='msle',optimizer=SGD(lr = 0.01))
    model.fit(train_X_expanded, train_y, epochs=200, batch_size=10, verbose=0)
    model.save("studen_deep_linear.h5")
    '''
    #sklearn機器學習的線性回歸
    model = LinearRegression()
    model.fit(train_X_expanded, train_y)
    studen_learning_curve(model , X_expanded , y)
    
    #分析
    pred = model.predict(X_expanded) 
    X = X * (max_features-min_features) + min_features
    y = y * (max_labels-min_labels) + min_labels
    #test_X = test_X * (max_features-min_features) + min_features
    train_X = train_X * (max_features-min_features) + min_features
    pred = pred * (max_labels-min_labels) + min_labels
    draw_data(X , y , X , pred)
    return model

def studen_deep_suggest(X, y , n_days): #使用模型做預測做推薦
    from keras.models import load_model
    import numpy as np
    from sklearn.linear_model import LinearRegression
    #from keras.layers import Dense, Activation, Dropout
    #from keras.optimizers import SGD, Adam
    
    n = 20 #10項式
    suggest = np.arange(200, 200 + n_days).reshape(n_days, 1) #產生x座標來預測
    
    #資料標準化
    max_labels_x, min_labels_x = max(X), min(X)
    X = (X-min_labels_x)/(max_labels_x-min_labels_x)
    max_features, min_features = max(suggest), min(suggest)
    suggest = (suggest-min_features)/(max_features-min_features)
    max_labels, min_labels = max(y), min(y)
    y = (y-min_labels)/(max_labels-min_labels)
    
    #資料多項式處理化
    from sklearn.preprocessing import PolynomialFeatures
    poly_features = PolynomialFeatures(degree = n, include_bias=False)
    train_X_expanded = poly_features.fit_transform(X)
    suggest_expanded = poly_features.fit_transform(suggest)
    
    #模型
    #model = load_model("studen_deep_linear.h5")
    #model.fit(train_X_expanded, train_y)
    #studen_learning_curve(model, X_expanded , y)
    model = LinearRegression()
    model.fit(train_X_expanded, y)
    
    #分析
    pred = model.predict(suggest_expanded)
    X = X * (max_labels_x-min_labels_x) + min_labels_x
    y = y * (max_labels-min_labels) + min_labels
    suggest = suggest * (max_features-min_features) + min_features
    pred = pred * (max_labels-min_labels) + min_labels
    draw_data(X , y , suggest , pred)
    return X , y , suggest , pred