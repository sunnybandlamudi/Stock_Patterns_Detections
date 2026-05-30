from curl_cffi import requests
import datetime
import calendar
from dotmap import DotMap
import csv
import json

sortValue = 'g'
CALL = "CE"
PUT = "PE"
stock = 'RELIANCE'
expire_month = 0
buy_price = 1225
number_of_shares = 500

# URLs
fno_lot_url = "https://nsearchives.nseindia.com/content/fo/fo_mktlots.csv"
CONTRACT_INFO_URL = "https://www.nseindia.com/api/option-chain-contract-info"
OPTION_CHAIN_V3_URL = "https://www.nseindia.com/api/option-chain-v3"

session = requests.Session()
session.get("https://www.nseindia.com/", impersonate="chrome110")


def get_fno_lot_size():
    response = session.get(fno_lot_url, impersonate="chrome110")
    data_dict = {}

    csv_data = response.text.splitlines()
    csv_reader = csv.reader(csv_data[:])

    for row in csv_reader:
        if len(row) >= 3:
            key = row[1].strip()
            value = row[2].strip()
            if value.isnumeric():
                data_dict[key] = int(value)

    return data_dict


# Getting fno lot size
fno_lot = get_fno_lot_size()


def get_option_chain(stock):
    session.get("https://www.nseindia.com/", impersonate="chrome110")

    # Get available expiry dates
    info = session.get(CONTRACT_INFO_URL, params={"symbol": stock}, impersonate="chrome110")
    expiry_dates = info.json()["expiryDates"]
    expire = expiry_dates[expire_month]
    print(f'Getting option data for {expire}')

    # Get option chain for that expiry
    data = session.get(OPTION_CHAIN_V3_URL,
                       params={"type": "Equity", "symbol": stock, "expiry": expire},
                       impersonate="chrome110")
    return DotMap(data.json())


def get_option_data(opt, itr):
    return [val for val in map(lambda key: key.get(opt), itr) if
            bool(val) and val.get('strikePrice') > val.get('underlyingValue')]


def call_spread(call_data):
    list_data = []
    for data in call_data:

        current = data.underlyingValue
        strike_price = data.strikePrice
        if strike_price > current:
            lot_size = fno_lot[data.underlying]
            ask, bid = (data.buyPrice1, data.sellPrice1)

            equity_profit = (current - buy_price) * number_of_shares
            fno_profit = ask * lot_size
            real_square_off_profit = ((strike_price + ask - buy_price) * number_of_shares) - fno_profit
            profit_for_1_lot = ((strike_price + ask - buy_price) * lot_size)

            fno_break_even = strike_price + ask
            rr_fno = fno_profit * 100 / (number_of_shares * buy_price)
            rr_stock = real_square_off_profit * 100 / (number_of_shares * buy_price)
            percent_change = (strike_price + ask - buy_price) * 100 / buy_price

            list_data.append({
                "STRIKE_PRICE": strike_price,
                "CALL_PRICE": ask,
                "FNO_BE": fno_break_even,
                "EQUITY_PROFIT": equity_profit,
                "FNO_PROFIT": fno_profit,
                "REAL_PROFIT": real_square_off_profit,
                "PROFIT/LOT": profit_for_1_lot,
                "RR_FNO": rr_fno,
                "RR_STOCK": rr_stock,
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
            break
        elif sort_value == 'get' or sort_value == 'g':
            option_data = get_option_chain(stock)
            option_records = option_data.records.data

            opt_data = list(filter(lambda data: data.expiryDates.upper() == option_data.records.expiryDates[expire_month].upper(), option_records))
            call_data = get_option_data(CALL, opt_data)
            putData = get_option_data(PUT, opt_data)

            ord_list = call_spread(call_data)
            print_data(ord_list)

        else:
            ord_list = sorted(ord_list, key=lambda itr: sort(itr, sort_value))
            print_data(ord_list)
        print("Enter sorting value ", end=' ')
        sort_value = input()


def sort(itr, sort_value):
    return list(itr.values())[int(sort_value) - 1]


main()
