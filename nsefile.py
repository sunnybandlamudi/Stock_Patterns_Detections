import requests
import csv
import json
from nsedata import *

# URL of the CSV file
fno_lot_url = "https://nsearchives.nseindia.com/content/fo/fo_mktlots.csv"
index_url = 'https://www.nseindia.com/api/equity-stockIndices'


def get_fno_lot_size():
    
    data_dict = {}
    # Send an HTTP GET request to the URL
    response = get_nse_data(fno_lot_url)

    # Parse the CSV content
    csv_data = response.splitlines()
    csv_reader = csv.reader(csv_data[:])

    for row in csv_reader:
        if len(row) >= 3:
            key = row[1].strip()
            value = row[2].strip()
            if(value.isnumeric()):
                data_dict[key] = int(value)

    # Print the key-value pairs
    # for key, value in data_dict.items():
        #     print(f"{key}: {value}")
    return data_dict


def get_index_data():
    
    nse_dict = get_fno_lot_size()
    
    params = {
            'index': 'NIFTY 50'
        }

    response = get_nse_data(index_url,params=params)

    index_data = json.loads(response)
    for data in index_data['data']:
        # print(data['symbol'])
        try:
            symbol, lot_size, last_price = data['symbol'], int(nse_dict[data['symbol']]), data['lastPrice']
            cal_price = (lot_size * last_price)/4
            if cal_price > 50000 and cal_price < 150000:
                print('{: <15}\t{: <15}\t{: <15}'.format(symbol, lot_size, cal_price))
        except Exception as e:
            print(e)
            pass

def calcuate_stock():
    index_data = get_index_data()

# calcuate stock
calcuate_stock()

