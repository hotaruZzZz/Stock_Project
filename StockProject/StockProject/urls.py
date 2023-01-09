from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('stock_data/', include('stock_data.urls')),
    path('accounts/', include('allauth.urls')),  # django-allauth網址
]
