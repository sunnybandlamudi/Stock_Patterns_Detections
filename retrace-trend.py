from nsetools import nse;
from nse import Nse
from matplotlib import pyplot as plt
import numpy as np;
import pandas as pd
import requests as req;
from datetime import date,timedelta;
import math #needed for definition of pi




def get_historic_data(stock):
    params = {
        'symbol':stock,
        'series':'["EQ"]',
        'from': (date.today() - timedelta(days=90)).strftime("%d-%m-%Y"),
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

    x= df['CH_TIMESTAMP'][::]
    y= df['CH_CLOSING_PRICE'][::]
    z = df['CH_TRADE_HIGH_PRICE'][::]
    return  list(zip(x,y,z))


def getMaxPoint(mapping):
    maxpoint = None;
    maxpointIndex = None;
    for i in range(len(mapping)-30):
        rightMax = max(mapping[0:i+3], key = lambda item : item[2]);
        leftMax = max(mapping[i+3:i+20], key = lambda item : item[2]);
        if(rightMax[2] > leftMax[2]):
            maxpoint = rightMax;
            maxpointIndex = mapping.index(maxpoint);
    mn = [];
    for j in range(maxpointIndex+2,len(mapping)-30):
        if( (mapping[j-1][1] > mapping[j][1] < mapping[j+1][1]) and (mapping[j-2][1] > mapping[j][1] < mapping[j+2][1])):
            localMin = mapping[j]
            mn.append(localMin)

    if(mn[0][1] > mn[1][1]):
        localMin = mn[0];
    else:
        localMin = None;
    return maxpoint,localMin;

head = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
}

req = req.Session()
req.get('https://www.nseindia.com',headers=head)
# req.get('https://www.nseindia.com',headers=head)


db = Nse()
fno = nse.Nse()
fno_lot = fno.get_fno_lot_sizes(as_json=False);
fno_list= list(fno_lot.keys())

global df,historic_data,x,y,mapping,mn,mx, maxY,minY ,mindate, maxdate, closingPrice,STOCK
for stk in fno_list:
    try:
        mapping = getMaxMin(stk);
        #print(mapping)
        maxpoint,localMin = getMaxPoint(mapping);

        if(maxpoint ):
            currentPercentage = ((maxpoint[2])-(mapping[0][2]))*100/maxpoint[2];
            if(localMin):
                swingPercentage = ((maxpoint[1])-(localMin[1]))*100/localMin[1];
            if(currentPercentage > 1 and swingPercentage > 5):
                print("\nStock: {} \nHigh: {} \nCurrent: {} \nLow: {}\nSwing High  {} \t Swing Low  {}".format(stk,maxpoint,mapping[0],localMin,swingPercentage,currentPercentage))
    except:
        print(stk);
        



    


