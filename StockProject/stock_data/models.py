from django.db import models
from django.contrib import admin


# Create your models here.

class Data(models.Model):
    sName = models.CharField(max_length = 20)
    sNumber = models.CharField(max_length = 20)
    sDate =  models.DateField(null=False)
    sOpen = models.DecimalField(max_digits=20,decimal_places=2)
    sHigh = models.DecimalField(max_digits=20,decimal_places=2)
    sLow = models.DecimalField(max_digits=20,decimal_places=2)
    sClose = models.DecimalField(max_digits=20,decimal_places=2)

    def __str__(self):
        return self.sName


@admin.register(Data)
class DataAdmin(admin.ModelAdmin):
    list_display = ['id', 'sDate','sName', 'sNumber', 'sOpen', 'sHigh', 'sLow', 'sClose']
    search_fields = ('sDate', 'sName', 'sNumber')#search
    ordering = ('sDate',)#以日期排序





