from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

from .forms import DataForm
from .models import Data, Stock, Focus, MonthlyRevenue, User
from .filters import DataFilter,StockFilter,FocusFilter
from .scrapers import TWSE

from django.contrib.auth.decorators import login_required
from .forms import RegisterForm

import twstock #台股
import matplotlib.pyplot as plt
import plotly.graph_objs as go
from plotly.offline import plot
import time
from datetime import date,timedelta
import pandas as pd
from pandas import DataFrame
from dateutil.relativedelta import relativedelta

from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger

from pandas import DataFrame
import numpy as np
import pymysql
from deeplearn import studen_suggest
import matplotlib.pyplot as plt
import plotly.graph_objs as go
from plotly.offline import plot


#首頁
def home(request):
    user = request.user #登入的使用者
    datas  = Focus.objects.filter(user_id=user.id) #取得使用者id抓取紀錄
    data = datas.values('stock_code').distinct() #去除重複資料
    today = date.today() #今天日期
    while(Data.objects.filter(sDate=today).exists() == False): #假如沒當天資料
        today -= timedelta(days=1) #減一天
    sdate = str(today) #將日期格式轉為字串
    rank1 = Data.objects.filter(sDate=sdate).order_by('-sTradeVolume')[0:9] #已成交股數排名    
    rank2 = Data.objects.filter(sDate=sdate).order_by('-sTransaction')[0:9] #以成交筆數排名    
    rank3 = Data.objects.filter(sDate=sdate).order_by('-sTradeValue')[0:9] #以成交價排名  

    #輸出給前端的資料
    context = {
        'data' : data, 
        'user' : user, 
        'rank1': rank1, 
        'rank2': rank2,
        'rank3': rank3,
        'date': sdate
        }
 
    return render(request, 'stock_datas/home.html',context)

#K線圖
def K(request):
    code = '' #股票代號
    plot_div = '' #圖表
    if request.method == "POST":
        code = request.POST.get("stock_number")

        plt.style.use('fivethirtyeight') #圖表樣式
        df = pd.DataFrame(Data.objects.filter(sNumber=code).values()) #取得資料
        #將資料轉為K線圖
        can =  go.Candlestick( 
                  x=df['sDate'],
                  open=df['sOpen'],
                  high=df['sHigh'],
                  low=df['sLow'],
                  close=df['sClose'],
                  increasing_line_color='red',
                  decreasing_line_color='green'
              )

        layout = go.Layout(
            title=code+'走勢圖',
               xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label="1m",
                     step="month",
                     stepmode="backward"),
                dict(count=6,
                     label="6m",
                     step="month",
                     stepmode="backward"),
                dict(count=1,
                     label="YTD",
                     step="year",
                     stepmode="todate"),
                dict(count=1,
                     label="1y",
                     step="year",
                     stepmode="backward"),
                dict(step="all")
            ])
        ),
        rangeslider=dict(
            visible=True
        ),
        type="date"
    ),
   width=1200, height=600

)
        config = dict({'scrollZoom': True})
        plot_div= plot({"data": [can], "layout": layout},output_type='div',config=config)   
        
    return render(request, 'stock_datas/K.html', context={'plot_div': plot_div})

#創建股票資料(用不到)
@login_required
def data_create_view(request):
    form = DataForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = DataForm() # 清空 form

    context = {
        'form' : form
    }
    return render(request, "stock_datas/data_create.html", context)

#查詢現有資料
def query(request):
    data = ''
    stock = ''
    code = ''
    sdate = time.strftime("%Y:%m:%d", time.localtime())
    if request.method == "POST":
        code = request.POST.get("code")
        sdate = request.POST.get("sdate")
        data = Data.objects.filter(sNumber=code,sDate=sdate)
        stock = Stock.objects.filter(code=code)
        print(sdate)
       
    context = {
        'data': data,
        'stock': stock,
        'date' : sdate,
        'code' : code
    }
 
    return render(request, 'stock_datas/stock_query.html', context)

#刪除資料
def delete(request, pk):

    stock_data = Data.objects.get(id=pk)

    if request.method == "POST":
        stock_data.delete()
        return redirect('/stock_data/query')

    context = {
        'stock_data': stock_data
    }

    return render(request, 'stock_datas/delete.html', context)

#查詢(爬蟲)
def search(request):

    twse = TWSE(request.POST.get("stock_number"))
    context = {
        "datas": twse.scrape() 
    }
    return render(request, 'stock_datas/stock_data_search.html', context)

#編輯股票資訊
def edit(request, pk):

    stock_data = Data.objects.get(id=pk)
    if request.method == "POST":
        stock_data.sName = request.POST['sNmae']
        stock_data.sNumber = request.POST['sNumber']
        stock_data.sDate = request.POST['sDate']
        stock_data.sOpne = request.POST['sOpen']
        stock_data.sHigh = request.POST['sHigh']
        stock_data.sLow = request.POST['sLow']
        stock_data.sClose = request.POST['sClose']
        stock_data.save()
        return redirect('/stock_data/query')
    context = {
        'stock_data': stock_data
    }
    return render(request, 'stock_datas/stock_data_edit.html', context)

#新增資料
def insert(request):
    if request.method == "POST":
        twse = TWSE(request.POST.get("stock_number"))
        data =twse.scrape_day() 
        for i in range(len(data)):
            stock = Data()
            stock.sDate = data[i]["sday"]
            stock.sName = data[i]['sname']
            stock.sNumber = data[i]['index']
            stock.sOpen = data[i]['sopen']
            stock.sHigh = data[i]['shigh']
            stock.sLow = data[i]['slow']
            stock.sClose = data[i]['sclose']
            stock.sVolume = data[i]['svolume']
            stock.save()
        return redirect('/stock_data/query')
    return render(request, 'stock_datas/stock_insert.html')

#登入
def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/index/')
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        auth.login(request, user)
        return HttpResponseRedirect('/index/')
    else:
        return render(request, 'login.html', locals())

def index(request):
    return render(request, 'index.html')

#登出
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/index/')

#編輯個人資訊
def user_edit(request):
    user = request.user #登入的使用者
    user_email = user.email #使用者的email
    context = {
        'user': user,
        'email' : user_email
    }
    return render(request, 'setting.html',context)


#重設密碼
def reset_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('/stock_data/accounts/setting/')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {
        'form': form
    })



#更改名稱
def change_name(request):
    user_name = request.user #登入的使用者
    user = User.objects.get(username = user_name)
    
    if request.method == 'POST':
        name = request.POST.get("user")
        user.username = name
        user.save()
        return redirect('/stock_data/accounts/setting/')
        
    context = {
        'user': user_name,
        
    }
    return render(request, 'change_name.html',context)

    

#登入畫面?
def register(request):

    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/stock_data/accounts/profile/')  #重新導向到登入畫面
    context = {
        'form': form
    }
    return render(request, 'register.html', context)

#更新資訊(用不到)
def update_code(request):
    if request.method == "POST":
        stock_data = twstock
        for i in stock_data.codes.keys():
            data = Stock.objects.create(code = stock_data.codes[i].code, name = stock_data.codes[i].name ,
                                       type  = stock_data.codes[i].type, ISIN = stock_data.codes[i].ISIN,
                                       market = stock_data.codes[i].market, group = stock_data.codes[i].group)
            data.save() 
            #print(stock_data.codes[i].name + ' ' + stock_data.codes[i].code + ' ' + stock_data.codes[i].market)
        return  redirect('/stock_data')
    return render(request, 'stock_datas/data.html')

#股票公司詳細資訊            
def stock_information(request):

    #datas = Stock.objects.all()
    #dataFilter = StockFilter(queryset=datas)
    code = request.POST.get("stock_number")
    stock_data = Stock.objects.filter(code=code)
    
    context = {
        'data': stock_data
    }
    return render(request, 'stock_datas/stock_information.html',context)

#關於
def about(request):
     return render(request, 'stock_datas/about.html')


@login_required #登入才能使用
def focus(request):
    user = request.user #登入的使用者
    code = request.POST.get("stock_number") #輸入的股票代號
    datas  = Focus.objects.filter(user_id=user.id) #取得使用者id抓取紀錄
    data = datas.values('stock_code').distinct() #去除重複資料
    
    #all_code = datas.stock_code
    #focusFilter = datas.objects.filter(pk=code)
    if request.method == "POST":
        f = Focus()
        f.user_id = user.id
        f.stock_code = code
        f.save()
        return redirect('/stock_data/focus')
    context = {
        'data': data,
    }
    return render(request, 'stock_datas/focus.html', context)

#刪除所選關注中的資料
def focus_delete(request, code):
    user = request.user #登入的使用者
    Focus.objects.filter(user_id=user.id,stock_code=code).delete() #取得使用者id抓取紀錄

    return redirect('/stock_data/focus')

def market(request):
    return render(request, 'stock_datas/market.html')

#上市股票(Listed)
def listed(request):
    datas  = Stock.objects.filter(market='上市')
    context = {
        'data': datas
    }
    return render(request, 'stock_datas/listed.html', context)

#上櫃股票(OTC)
def otc(request):
    datas  = Stock.objects.filter(market='上櫃')
    context = {
        'data': datas
    }
    return render(request, 'stock_datas/otc.html', context)   

#所有連結
def link(request):
    return render(request, 'stock_datas/link.html')

#個股資料大整合
def stockIfo(request, code):
    code = code
    stock_data = Stock.objects.filter(code=code)
    plt.style.use('fivethirtyeight')
    df = pd.DataFrame(Data.objects.filter(sNumber=code).values())
    can =  go.Candlestick(
                  x=df['sDate'],
                  open=df['sOpen'],
                  high=df['sHigh'],
                  low=df['sLow'],
                  close=df['sClose'],
                  increasing_line_color='red',
                  decreasing_line_color='green'
              )

    volume = go.Bar(
            x=df['sDate'],
            y=df['sTradeVolume'],
            showlegend=False,
            marker={
        "color": "rgba(128,128,128,0.5)",
    }
            )

    layout = go.Layout(
            title=code+'走勢圖',
               xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label="1m",
                     step="month",
                     stepmode="backward"),
                dict(count=6,
                     label="6m",
                     step="month",
                     stepmode="backward"),
                dict(count=1,
                     label="YTD",
                     step="year",
                     stepmode="todate"),
                dict(count=1,
                     label="1y",
                     step="year",
                     stepmode="backward"),
                dict(step="all")
            ])
        ),
        rangeslider=dict(
            visible=True
        ),
        type="date"
    ),
   width=800, height=600
   

)
    config = dict({'scrollZoom': True})
    plot_div= plot({"data": [can], "layout": layout},output_type='div',config=config)   
    context = {
        'data': stock_data,
        'plot_div': plot_div,
        'code': code
    }
    return render(request, 'stock_datas/stockIfo.html',context)

#月報表
def monthly(request):

    today = date.today()
    while(MonthlyRevenue.objects.filter(Myear=str(int(today.year) - 1911),Mmonth=str(today.month)).exists() == False):
        today -= relativedelta(months=1)
        
    year = str(int(today.year)-1911)
    month = str(today.month)
    #print(year,month)   
    data = MonthlyRevenue.objects.filter(Myear=year, Mmonth=month)
    if request.method == "POST":
        year  = request.POST.get("year")
        month  = request.POST.get("month")
        data = MonthlyRevenue.objects.filter(Myear=year, Mmonth=month)
    context = {
        'data': data,
        'year': year,
        'month': month
    }
    
    return render(request, 'stock_datas/month.html',context)

#個股月報表
def all_monthly(request, code):
    data = MonthlyRevenue.objects.filter(month_code=code)
    code =code
    context = {
        'data': data,
        'code': code
    }
    return render(request, 'stock_datas/all_month.html',context)

#預測股票
def predict(request):
    code = ''
    name = ''
    plotly_div = ''
    data = []
    result = ''
    db = pymysql.connect(host='localhost', port=3306, user='test', passwd='1234123zxc', db='django', charset='utf8')
    cursor = db.cursor()


    if request.method == "POST":

        #SQL語法
        sql = (
            "select * from stock_data_data where sDate > '2014-01-01' and sNumber = '0056' and sClose != (-1.00) order by sDate;")#執行語法
        print(sql)
        try:
          cursor.execute(sql)
          result = DataFrame(cursor.fetchall())
          data = result
          if data.empty == True:
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
        first_data , first_add_data , pred_0056 , train_0056 = studen_suggest.suggest_start(data, len(data) , 0)
        code = request.POST.get("stock_number")
        name = Stock.objects.filter(code=code)
        suggest_list = np.zeros((1,2))
        data = []
        #建立操作游標
        cursor = db.cursor()
        #SQL語法
        sql = (
            "select * from stock_data_data where sDate > '2014-01-01' and sNumber = '"
            + code +
            "' and sClose != (-1.00) order by sDate;"
            )#執行語法
        print(sql)
        try:
            cursor.execute(sql)
            result = DataFrame(cursor.fetchall())
            data = result
            
            if data.empty == True:
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
        print("--------------------------start")
        suggest , number1, number2, plotly_div, result = studen_suggest.suggest_start(data, len(data),1 , first_data , first_add_data , train_0056 , pred_0056)
        print("--------------------------end")
    return render(request, 'stock_datas/predict.html', context={'name':name,'plot_div': plotly_div, 'result':result})

#股票排名
def rank(request):
    today = date.today()
    while(Data.objects.filter(sDate=today).exists() == False):
        today -= timedelta(days=1)
    sdate = str(today)
    data = Data.objects.filter(sDate=sdate).order_by('-sTradeVolume')[0:9] #已成交股數排名
    rank = '-sTradeVolume'
    record = 10

    if request.method == "POST":
        sdate = request.POST.get("date")
        rank = request.POST.get("rank")
        record = request.POST.get("records")
        record = int(record) 
        data = Data.objects.filter(sDate=sdate).order_by(rank)[0:record] #已成交股數排名
        print(sdate,rank,record)
    context = {
        'data': data,
        'date': sdate,
        'record': record
    }
    return render(request, 'stock_datas/rank.html',context)

#推薦股票
def predict_rank(request):

    db = pymysql.connect(host='localhost', port=3306, user='test', passwd='1234123zxc', db='django', charset='utf8')
    cursor = db.cursor()
    s = "select distinct(sNumber) from stock_data_data where sDate > '2022-11-01'  and sClose != (-1.00);"
    list_id = []
    suggest_id = ['2603'
                ,'3034'
                ,'2454'
                ,'2382'
                ,'2357'
                ,'2409'
                ,'4938'
                ,'3711'
                ,'2324'
                ,'2347'
                ,'2301'
                ,'1102'
                ,'2303'
                ,'1402'
                ,'3231'
                ,'2356'
                ,'3702'
                ,'2891'
                ,'2379'
                ,'2377'
                ,'2027'
                ,'8046'
                ,'2890'
                ,'2317'
                ,'2885'
                ,'2474'
                ,'1301'
                ,'1303'
                ,'4958'
                ,'2376'
                ,'2385'
                ,'2337'
                ,'6239'
                ,'2383'
                ,'1802'
                ,'2915'
                ,'3036'
                ,'2542'
                ,'3044'
                ,'6176'
                ,'3189'
                ,'2637'
                ,'2449'
                ,'5522'
                ,'2606'
                ,'3017'
                ,'2006'
                ,'2809'
                ,'3665'
                ,'6271']
    number_list = []
    best = ''
    plotly = []
    result_plotly = []
    result = ''
    temp = 0
    cursor = db.cursor()
    #SQL語法
    sql = (
        "select * from stock_data_data where sDate > '2014-01-01' and sNumber = '"
        + '0056' +
        "' and sClose != (-1.00) order by sDate;"
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
  
    #print(data)#close = np.array(data)
    #close = data[7]
    first_data , first_add_data , pred_0056 , train_0056 = studen_suggest.suggest_start(data, len(data) , 0)
    try:
        cursor.execute(s)
        list_id = DataFrame(cursor.fetchall())
        db.commit()
        print('success')
    except:
      #發生錯誤時停止執行SQL
      db.rollback()
      print('error')    

    if request.method == "POST":
        list_id = list_id.values
        print(list_id)
        

        for i in suggest_id:     

            data = []
            db = pymysql.connect(host='localhost', port=3306, user='test', passwd='1234123zxc', db='django', charset='utf8')
            #建立操作游標
            cursor = db.cursor()
            #SQL語法
            sql = (
                "select * from stock_data_data where sDate > '2014-01-01' and sNumber = '"
                + str(i) +
                "' and sClose != (-1.00)  order by sDate ;"
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
            #train_0056, pred_0056= studen_suggest.suggest_start(data, len(data) , 0)
            max_number = 0
            max_id = '0'
            #suggest_list = []
            
            suggest , number1, number2, plotly_1, plotly_2 = studen_suggest.suggest_start(data, len(data),1 , first_data , first_add_data , train_0056 , pred_0056)
            #suggest , number1, number2, plotly_1, plotly_2 = studen_suggest.suggest_start(data, len(data),1 , train_0056 , pred_0056)
            number_list.append((i , number1[0] , number2[0]))
            plotly.append(plotly_1)
            result_plotly.append(plotly_2)

        max_number = 0
        t = 0

        for i in number_list:
            #print(type(i[0]) , i[0])
            if max_number < (i[1]-i[2]):
                max_number = (i[1]-i[2])
                max_id = i[0]  
                temp = t
                t += 1

            else:
                t += 1


        plot_div = plotly[temp]
        plot_div_result = result_plotly[temp]
        best = Stock.objects.filter(code=max_id)
        #print(number_list)
        print("suggest:\n------" ,max_id,'------\n')
        number_list.sort(key=lambda x:x[1])
        print(number_list)
        number_list = number_list[::-1]

        
    else:
        plot_div = ''
        plot_div_result = ''
    context = {
        'best' : best,
        'plot_div': plot_div,
        'result' : plot_div_result,
        'data': number_list[:10]
        }

    return render(request, 'stock_datas/predict_rank.html', context) 