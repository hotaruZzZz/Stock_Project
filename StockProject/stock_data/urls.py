from django.contrib import admin
from django.urls import path, include
from .import views
from stock_data.views import login, index, logout, register
from django.contrib.auth import views as aViews
from .pyechart import site_obj

urlpatterns = [
    path('', views.home, name="Home"), #首頁
    path('home', views.home, name="Home"), #首頁 
    path('query',views.query, name="Query"), #個股資料查詢
    path('index/', index), #歡迎畫面
    path('accounts/login/', aViews.LoginView.as_view(), name='login'), #登入
    path('accounts/logout/', aViews.LogoutView.as_view(), name='logout'), #登出
    path('accounts/setting/', views.user_edit, name='user_edit'), #設定
    path('accounts/setting/reset_password/', views.reset_password, name='reset_password'), #改密碼
    path('accounts/setting/change_name/', views.change_name, name='change_name'), #改名字
    path('accounts/profile/', index), #歡迎畫面
    path('accounts/register/', register), #註冊
    path('stock_information', views.stock_information, name='Information'), #股票公司資訊
    path('about', views.about, name='About'), #關於
    path('focus', views.focus, name='Focus'), #關注
    path('focus_delete/<str:code>', views.focus_delete, name='focus_delete'), #取消關注
    path('K', views.K, name='K'), #K線圖
    path('market', views.market, name='Markte'), #公司類型
    path('market/listed', views.listed, name='Listed'), #上市
    path('market/otc', views.otc, name='OTC'), #上櫃
    path('stockIfo/<str:code>', views.stockIfo, name='Ifo'), #個股詳細資訊
    path('monthly', views.monthly, name='Monthly'), #月報表
    path('stockIfo/<str:code>/all_monthly', views.all_monthly, name='AllMonthly'), #個股月報表
    path('predict', views.predict, name='Predict'), #預測股票
    path('rank', views.rank, name='Rank'), #股票排名
    path('predict_rank', views.predict_rank, name='PredictRank'), #推薦股票
         ]

    #path('create', views.data_create_view), # 新增
    #path('delete/<str:pk>', views.delete, name='Delete'),    
    #path('search', views.search, name='Search'),  
    #path('edit/<str:pk>', views.edit, name='Edit'),  
    #path('insert', views.insert, name='Insert'),
    #path('data/', views.update_code), #爬股票資料用，只會用到一次，除非資料不見
    #path('site', include(site_obj.urls)),
    #path('link', views.link, name='Link'),