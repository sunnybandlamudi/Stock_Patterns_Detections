
from nse import Nse
from pprint import pprint;
import requests as req;
from nsetools import nse
import datetime
import calendar
import json;
head = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36"
}
call="CE"
put="PE"
sortValue = 'get'
stock = 'SBIN'
expire = '24-Sep-2020'
ord_list=[];
buyPrice = 200
averageLot = 3000;
stratagy = 1


# Getting fno lot size
fno = nse.Nse()
fno_lot = fno.get_fno_lot_sizes(as_json=False);


def get_optionchain(stock):
    data = req.get('https://www.nseindia.com/api/option-chain-equities', params={'symbol':stock}, headers = head)
    # pprint(data.json()['filtered'])
    return data.json()['records']

def getOptData(opt, itr):
    return [val for val in map(lambda key: key.get(opt) , itr) if bool(val) and val.get('strikePrice') > val.get('underlyingValue') ]

def calc_data(opt_data, strat = False):
    list_data = []
    
    for i in range(len(opt_data)):
        for j in range(i+1,len(opt_data)):
            current = opt_data[i]['underlyingValue']
            lot_size = fno_lot[opt_data[i]['underlying']]
            sellStrike,buyStrike = (opt_data[i]['strikePrice'],opt_data[j]['strikePrice'])
            ask,bid= (opt_data[i]['bidprice'],opt_data[j]['askPrice'])
            exp = opt_data[i]['expiryDate']
            breakEven = sellStrike+ask-bid
            profit = (ask-bid) * lot_size
            loss= ((buyStrike-sellStrike)*lot_size - profit)*-1
            rR = abs(profit/loss)
            if(strat):
                if (breakEven - buyPrice)*averageLot + loss> 0:
                    upProfit=(breakEven - buyPrice)*averageLot + (loss);
                    list_data.append({"Expire":"{}-{}".format(current,exp.split('-')[1]),"Sell S":sellStrike,"Buy S":buyStrike,"BreakEven":breakEven,"Down":profit,"Up":upProfit,"Loss":loss,"RR":rR})
                    # print('profit value ',sellStrike,buyStrike, upProfit)
                    # list_data.append(('{}-{}'.format(current,exp.split('-')[1]),sellStrike,buyStrike,ask,bid,breakEven,profit,loss,rR))
            else:
                list_data.append({"Expire":"{}-{}".format(current,exp.split('-')[1]),"Sell S":sellStrike,"Buy S":buyStrike,"Ask": ask,"Bid":bid,"BreakEven":breakEven,"Profit":profit,"Loss":loss,"RR":rR})
                
    return list_data

def print_data(list_data):
    print(str("{:<20}"+"{:<10}"*(len(list_data[0].keys())-2)+"{:>10}").format(*list_data[0].keys()))
    for i in list_data:
        print(str("{:<20}"+"{:<10,.2f}"*(len(i)-2)+"{:>10.2f}").format(*i.values()))
        # print(("{:<20}"+"{:<10,.2f}"*len(i)-1).format(*i))
        #.format(*i))


while True:
    if sortValue == 'exit' or sortValue == 'e':
        break;
    elif sortValue == 'get' or sortValue == 'g':
        option_data= get_optionchain(stock);
        print('Getting option data done')
        option_data=option_data['data']
        opt_data = list(filter(lambda data : data['expiryDate']==expire,option_data))
        callData = getOptData(call,opt_data)
        putData =  getOptData(put,opt_data)
        ord_list = calc_data(callData,stratagy)
        print_data(ord_list)

    else:
        ord_list=sorted(ord_list,key=lambda itr: itr[int(sortValue)-1])
        print_data(ord_list)
    print("Enter sorting value ",end=' ');
    sortValue = input()






