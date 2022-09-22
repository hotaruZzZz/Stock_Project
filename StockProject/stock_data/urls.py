from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.showtemplate, name="showtemplate"),
    path('create', views.data_create_view), # 新增
    path('query',views.query, name="Query"),
    path('delete/<str:pk>', views.delete, name='Delete'),    
    path('search', views.search, name='Search'),  
    path('edit/<str:pk>', views.edit, name='Edit'),  
    path('insert', views.insert, name='Insert'),
    
]