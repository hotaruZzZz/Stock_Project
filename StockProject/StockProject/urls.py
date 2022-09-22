from django.contrib import admin
from django.urls import path,include
from StockProject.views import login, index, logout
from django.contrib.auth import views
from stock_data.views import register

urlpatterns = [
    path('admin/', admin.site.urls),
    path('stock_data/', include('stock_data.urls')),
    path('index/', index),
    path('accounts/login/', views.LoginView.as_view(), name='login'),
    path('accounts/logout/', views.LogoutView.as_view(), name='logout'),
    path('accounts/profile/', index),
    path('accounts/register/', register),
]
