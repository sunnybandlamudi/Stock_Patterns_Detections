from nse import Nse
from pprint import pprint;
import requests as req;
from nsetools import nse
import json;


def printStocks(ord_list):
    for lis in ord_list:
        print("{:<15}{:<10}{:<10}{:<15}{:<10}{:+,.2f}".format(*lis))

db = Nse()
fno = nse.Nse()
fno_lot = fno.get_fno_lot_sizes(as_json=False);
fno_list= list(fno_lot.keys())

head = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
}

ord_list= []

sortValue ='get'
while True:
    
    if sortValue == 'exit' or sortValue == 'e':
        break;
    elif sortValue == 'get' or sortValue == 'g':
        ord_list= []
        for syb in fno_list[2:]:
            res = req.get('https://www.nseindia.com/api/quote-derivative',params={'symbol':syb}, headers=head)
            stock_info=json.loads(res.text)
            arbi= (stock_info['stocks'][0]['metadata']['lastPrice']-stock_info['underlyingValue'])*100/stock_info['stocks'][0]['metadata']['lastPrice']
            printStocks([(stock_info['info']['symbol'],stock_info['underlyingValue'],int(fno_lot[syb]),stock_info['underlyingValue']*fno_lot[syb],stock_info['stocks'][0]['metadata']['lastPrice'],arbi)])
            ord_list.append((stock_info['info']['symbol'],stock_info['underlyingValue'],int(fno_lot[syb]),stock_info['underlyingValue']*fno_lot[syb],stock_info['stocks'][0]['metadata']['lastPrice'],arbi))
            # print(stock_info['info']['symbol'].ljust(20),str(stock_info['underlyingValue']).ljust(10),str(fno_lot[syb]).ljust(10),"{:,}".format(stock_info['underlyingValue']*fno_lot[syb]).ljust(20),str(stock_info['stocks'][0]['metadata']['lastPrice']).ljust(10),"{:.2f}".format(arbi))
            # pprint(stock_info['info']['symbol'],stock_info['underlyingValue'])

    else:    
        ord_list=sorted(ord_list,key=lambda itr: itr[int(sortValue)-1])
        printStocks(ord_list)
    print('Enter sorting index',end=' ')
    sortValue = input().strip();
    

# data = json.loads(res.text)['data']

# pprint(len(data))
# 
# for stock in data:
#     print(str(stock["meta"]["symbol"]).ljust(20),str(stock["lastPrice"]).ljust(20),str(stock["underlyingValue"]).ljust(20),(stock["lastPrice"]-stock["underlyingValue"])*100/stock["lastPrice"])
