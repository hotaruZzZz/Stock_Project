from django.shortcuts import render, redirect
from .forms import DataForm
from .models import Data
from .filters import DataFilter
from django.contrib.auth.forms import UserCreationForm
from .scrapers import TWSE


# Create your views here.
def showtemplate(request):
    stock_list = Data.objects.all() # 把所有 Data 的資料取出來
    context = {'stock_list': stock_list} # 建立 Dict對應到Data的資料，
    return render(request, 'stock_datas\stock_data_detail.html', context)


def data_create_view(request):
    form = DataForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = DataForm() # 清空 form

    context = {
        'form' : form
    }
    return render(request, "stock_datas/data_create.html", context)

def query(request):

    datas = Data.objects.all()
    dataFilter = DataFilter(queryset=datas)
 
    if request.method == "POST":
        dataFilter = DataFilter(request.POST, queryset=datas)
 
    context = {
        'dataFilter': dataFilter
    }
 
    return render(request, 'stock_datas/stock_query.html', context)

def delete(request, pk):

    stock_data = Data.objects.get(id=pk)

    if request.method == "POST":
        stock_data.delete()
        return redirect('/stock_data/query')

    context = {
        'stock_data': stock_data
    }

    return render(request, 'stock_datas/delete.html', context)

def search(request):

    twse = TWSE(request.POST.get("stock_number"))
    context = {
        "datas": twse.scrape() 
    }
    return render(request, 'stock_datas/stock_data_search.html', context)

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
            stock.save()
        return redirect('/stock_data/query')
    return render(request, 'stock_datas/stock_insert.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return HttpResponseRedirect('/accounts/login/')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', locals())