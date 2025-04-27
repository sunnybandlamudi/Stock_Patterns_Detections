import platform

import requests as req;
import datetime
import calendar
from dotmap import DotMap;
import csv
import json;

head = {
    'authority': 'www.nseindia.com',
    'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
    'sec-ch-ua-mobile': '?0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'accept-language': 'en-US,en;q=0.9',
}


sortValue = 'g'
CALL = "CE"
PUT = "PE"
stock = 'RELIANCE'
expire_month = 0
buy_price = 1225
number_of_shares = 500



# URL of the CSV file
url = "https://nsearchives.nseindia.com/content/fo/fo_mktlots.csv"
index_url = 'https://www.nseindia.com/api/equity-stockIndices'

session = req.Session()
session.get('https://www.nseindia.com', headers=head)


def get_fno_lot_size():
    session = req.Session()
    # Send an HTTP GET request to the URL
    response = session.get(url, headers=head)

    # Check if the request was successful
    if response.status_code == 200:
        # Create a dictionary to store key-value pairs
        data_dict = {}

        # Parse the CSV content
        csv_data = response.text.splitlines()
        csv_reader = csv.reader(csv_data[:])

        for row in csv_reader:
            if len(row) >= 3:
                key = row[1].strip()
                value = row[2].strip()
                if (value.isnumeric()):
                    data_dict[key] = int(value)

        # Print the key-value pairs
        # for key, value in data_dict.items():
        #     print(f"{key}: {value}")
        return data_dict
    else:
        print("Failed to retrieve data from the URL.")

# Getting fno lot size
fno_lot = get_fno_lot_size();


def get_option_chain(stock):
    session = req.Session()
    session.get('https://www.nseindia.com/get-quotes/derivatives',params={'symbol': stock}, headers=head)
    data = session.get('https://www.nseindia.com/api/option-chain-equities', params={'symbol': stock}, headers=head)
    # pprint(data.json()['filtered'])
    return DotMap(data.json())


def get_option_data(opt, itr):
    return [val for val in map(lambda key: key.get(opt), itr) if
            bool(val) and val.get('strikePrice') > val.get('underlyingValue')]


def call_spread(call_data):
    list_data = []
    for data in call_data:

        current = data.underlyingValue
        strike_price = data.strikePrice
        # current = 1300
        if strike_price > current:
            lot_size = fno_lot[data.underlying]
            ask, bid = (data.bidprice, data.askPrice)

            equity_profit = (current - buy_price) * number_of_shares
            fno_profit = ask * lot_size
            real_square_off_profit = ((strike_price + ask - buy_price) * number_of_shares) - fno_profit
            profit_for_1_lot = ((strike_price + ask - buy_price) * lot_size)

            fno_break_even = strike_price + ask
            # hard_break_even = current + real_square_off_profit / (lot_size - number_of_shares)

            rr_fno = fno_profit * 100 / (number_of_shares * buy_price)
            rr_stock = real_square_off_profit * 100 / (number_of_shares * buy_price)
            percent_change = (strike_price + ask - buy_price) * 100 / buy_price

            list_data.append({
                "STRIKE_PRICE": strike_price,
                "CALL_PRICE": ask,
                "FNO_BE": fno_break_even,
                # "HARD_BE": hard_break_even,
                "EQUITY_PROFIT": equity_profit,
                "FNO_PROFIT": fno_profit,
                "REAL_PROFIT": real_square_off_profit,
                "PROFIT/LOT": profit_for_1_lot,
                "RR_FNO": rr_fno,
                "RR_STOCK": rr_stock,
                # "RR_FNO_STOCK": rr_fno/rr_stock,
                "PERCENT_CHANGE": percent_change,
            })

    return list_data


def print_data(list_data):
    try:
        print(str("{:<20}" + "{:<15}" * (len(list_data[0].keys()) - 2) + "{:>10}").format(*(f"{item}({index+1})" for index, item in enumerate(list_data[0].keys()))))
        for i in list_data:
            print(str("{:<20}" + "{:<15,.2f}" * (len(i) - 2) + "{:>10.2f}").format(*i.values()))
    except:
        print("index out of bound")


def main():

    sort_value = 'g'
    ord_list = []


    while True:
        if sort_value == 'exit' or sort_value == 'e':
            break;
        elif sort_value == 'get' or sort_value == 'g':
            option_data = get_option_chain(stock)
            expiry_dates = option_data.records.expiryDates
            expire = expiry_dates[expire_month]
            print(f'Getting option data done for {expire}')
            option_data = option_data.records.data

            opt_data = list(filter(lambda data: data.expiryDate.upper() == expire.upper(), option_data))
            call_data = get_option_data(CALL, opt_data)
            putData = get_option_data(PUT, opt_data)

            ord_list = call_spread(call_data)
            print_data(ord_list)

        else:
            ord_list = sorted(ord_list, key=lambda itr: sort(itr, sort_value))
            print_data(ord_list)
        print("Enter sorting value ", end=' ')
        sort_value = input()
        print_data(sort_value)





def sort(itr, sort_value):
    return list(itr.values())[int(sort_value) - 1]

main()
