from nsetools import nse;
from nse import Nse
from matplotlib import pyplot as plt
import numpy as np;
import pandas as pd
import requests as req;
from datetime import date;
from pprint import pprint;
import math #needed for definition of pi


head = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
}

req = req.Session()
req.get('https://www.nseindia.com',headers=head)
# req.get('https://www.nseindia.com',headers=head)


def get_historic_data(stock):
    params = {
        'symbol':stock,
        'series':'["EQ"]',
        'from': '17-11-2019',
        'to': date.today().strftime('%d-%m-%Y')
    }
    data = req.get('https://www.nseindia.com/api/historical/cm/equity',params = params,headers = head)

    # pprint(data.json())
    return data.json()['data']


def getMaxMin( STOCK , pmx = False ):
    historic_data = get_historic_data(STOCK)
    
    df = pd.DataFrame(historic_data)
    # x = np.arange(0, 5*1, 1)
    # y = ['2020-11-17','2020-11-16','2020-11-15','2020-11-14','2020-11-13']
    
    x= df['CH_TIMESTAMP'][::-1]
    y= df['CH_CLOSING_PRICE'][::-1]
    
    
    mapping = list(zip(x,y))
    
    mx = []
    mn = []
    
    # Checking whether the first point is  
    # local maxima or minima or neither  
    if(mapping[0][1] > mapping[1][1]):
        mx.append(mapping[0])
    elif(mapping[0][1] < mapping[1][1]):
        mn.append(mapping[0])
    for i in range(1,len(mapping)-1):
        if(mapping[i-1][1] > mapping[i][1] < mapping[i + 1][1]):
            mn.append(mapping[i])
    
        elif(mapping[i-1][1] < mapping[i][1] > mapping[i + 1][1]):
            mx.append(mapping[i])
    
    if(mapping[-1] > mapping[-2]):
        mx.append(mapping[-1])
    elif(mapping[-1] < mapping[-2]):
        mn.append(mapping[-1])
    
    # print(len(mn))
    
    closingPrice = y.tail(1).item();
    
    mindate = [t[0] for t in mn]
    minY = [t[1] for t in mn]
    
    maxdate = [t[0] for t in mx]
    maxY = [t[1] for t in mx]
    
    if(pmx):
        print(mx)
    for price in mx:
        val =  (closingPrice-price[1])*100/closingPrice
        if val > 1 and val < 5:
            print("Stock {0} change {1} date {2} price {3} currentprice {4}".format(STOCK,val,price[0],price[1],closingPrice))
        # plotGraph();


def plotGraph():
        plt.plot(x,y)
        plt.plot(mindate,minY)
        # c =0;
        # for i in range(len(mn)-1):
        #     for j in range(i,len(mn)):
        #         x = mn[i][0],mn[j][0]
        #         y = mn[i][1],mn[j][1];
        #         c+=1
        #         print(c)
        #         plt.plot(x,y)
        
        
        plt.xlabel("date")
        plt.ylabel("price")
        plt.title(STOCK);
        plt.xticks(x, rotation='vertical')
        # Pad margins so that markers don't get clipped by the axes
        plt.margins(0.2)
        plt.show()
        plt.plot(maxdate,maxY)
        df.plot(x='CH_TIMESTAMP',y = 'CH_CLOSING_PRICE')



db = Nse()
fno = nse.Nse()
fno_lot = fno.get_fno_lot_sizes(as_json=False);
fno_list= list(fno_lot.keys())

global df,historic_data,x,y,mapping,mn,mx, maxY,minY ,mindate, maxdate, closingPrice,STOCK  
for stk in fno_list:
    try:
        print("processing ... "+stk)
        getMaxMin(stk, True)
    except:
        print(stk)
