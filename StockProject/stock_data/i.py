#爬取股票資訊
import twstock 

stock_data = twstock
for i in stock_data.codes.keys():
    print(stock_data.codes[i].name + ' ' + stock_data.codes[i].code + ' ' + stock_data.codes[i].market)