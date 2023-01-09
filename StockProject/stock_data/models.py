from django.db import models
from django.contrib import admin
from django.contrib.auth.models import (
 BaseUserManager, AbstractBaseUser
)
from django.contrib.auth.models import User

# Create your models here.
#每日股票資料
class Data(models.Model):
    sName = models.CharField(max_length = 20) #證券名稱
    sNumber = models.CharField(max_length = 20) #證券代號
    sDate =  models.DateField(null=False) #日期
    sOpen = models.DecimalField(max_digits=20,decimal_places=2) #開盤價
    sHigh = models.DecimalField(max_digits=20,decimal_places=2) #最高價
    sLow = models.DecimalField(max_digits=20,decimal_places=2) #最低價
    sClose = models.DecimalField(max_digits=20,decimal_places=2) #收盤價
    sTradeVolume = models.IntegerField() #成交股數
    sTransaction = models.IntegerField() #成交筆數
    sTradeValue = models.DecimalField(max_digits=20,decimal_places=2) #成交金額
    sDir = models.CharField(max_length = 20) #漲跌(+/-)
    sChange = models.DecimalField(max_digits=20,decimal_places=2) #漲跌價差
    sLastBestBidPrice = models.DecimalField(max_digits=20,decimal_places=2) #最後揭示買價
    sLastBestBidVolume = models.IntegerField() #最後揭示買量
    sLastBestAskPrice = models.DecimalField(max_digits=20,decimal_places=2) #最後揭示賣價
    sLastBestAskVolume = models.IntegerField() #最後揭示賣量
    sPE = models.DecimalField(max_digits=20,decimal_places=2) #本益比



    def __str__(self):
        return self.sName
    class Meta:
        indexes = [
            models.Index(fields=['sNumber', 'sName'])
            
        ]


@admin.register(Data)
class DataAdmin(admin.ModelAdmin):
    list_display = ['id', 'sDate','sName', 'sNumber', 'sOpen', 'sHigh', 'sLow', 'sClose', 'sTradeVolume', 'sTransaction', 'sTradeValue', 'sDir', 'sChange', 'sLastBestBidPrice', 'sLastBestBidVolume', 'sLastBestAskPrice', 'sLastBestAskVolume', 'sPE']
    search_fields = ('sDate', 'sName', 'sNumber')#search
    ordering = ('sDate',)#以日期排序



class Comment(models.Model):
        
    class Meta:
        #ordering = ['date_time']
        permissions = (
            ("can_comment", "Can comment"),  # 只有一個權限時，千萬不要忘了逗號！
        )
#股票詳細資訊
class Stock(models.Model):
    code = models.CharField(max_length = 20, default='')
    name = models.CharField(max_length = 20, default='')
    type = models.CharField(max_length = 30, default='')
    ISIN = models.CharField(max_length = 20, default='')

    market = models.CharField(max_length = 20, default='')
    group = models.CharField(max_length = 20, default='')

    
@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ['code','name','type','ISIN','market','group']
    search_fields = ('code', 'name')#search
    ordering = ('code',)#以股票代號排順序
#關注清單
class Focus(models.Model):
    user_id = models.CharField(max_length = 20, default='')
    stock_code = models.CharField(max_length = 20, default='')

@admin.register(Focus)
class FocusAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'stock_code']
    search_fields = ('user_id', 'Stock_code')
    ordering = ('user_id' ,)

class MonthlyRevenue(models.Model):
    month_code = models.CharField(max_length = 20)
    month_name = models.CharField(max_length = 20)
    Myear =  models.CharField(max_length = 6) # 年分(民國)
    Mmonth = models.CharField(max_length = 3) #月份
    month_revenue = models.DecimalField(max_digits=20,decimal_places=2)
    month_lastrevenue = models.DecimalField(max_digits=20,decimal_places=2)
    month_lastyear = models.DecimalField(max_digits=20,decimal_places=2)
    month_lastmol = models.DecimalField(max_digits=20,decimal_places=2)
    month_samemol = models.DecimalField(max_digits=20,decimal_places=2)
    month_grand = models.DecimalField(max_digits=20,decimal_places=2)
    month_lastgrand = models.DecimalField(max_digits=20,decimal_places=2)
    month_forwardmol = models.DecimalField(max_digits=20,decimal_places=2)

    def __str__(self):
        return self.month_name


@admin.register(MonthlyRevenue)
class MonthlyRevenueAdmin(admin.ModelAdmin):
    list_display = ['id','month_code','month_name','Myear','Mmonth','month_revenue','month_lastrevenue','month_lastyear','month_lastmol'
                    ,'month_samemol','month_grand','month_lastgrand','month_forwardmol']
    search_fields = ('Myear','Mmonth','month_code')#search
    ordering = ('Myear',)#以日期排序


class TechnicalSide(models.Model):
    tdate = models.DateField(null=False) #日期
    tcode = models.CharField(max_length = 20) #證券代號
    ma5  = models.DecimalField(max_digits=20,decimal_places=2) #5移動平均
    ma10  = models.DecimalField(max_digits=20,decimal_places=2) #10移動平均
    ma20  = models.DecimalField(max_digits=20,decimal_places=2) #20移動平均

@admin.register(TechnicalSide)
class TechnicalSideAdmin(admin.ModelAdmin):
    list_display = ['id','tdate','tcode','ma5','ma10','ma20']
    search_fields = ('tdate','tcode')#search
    ordering = ('tdate',)#以日期排序
