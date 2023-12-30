import requests
import csv

# URL of the CSV file
url = "https://nsearchives.nseindia.com/content/fo/fo_mktlots.csv"
index_url = 'https://www.nseindia.com/api/equity-stockIndices'

head = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
}

session = requests.Session()
session.get('https://www.nseindia.com',headers=head)

def get_fno_lot_size():

    session = requests.Session()
    # Send an HTTP GET request to the URL
    response = session.get(url, headers= head)

    # Check if the request was successful
    if response.status_code == 200:
        # Create a dictionary to store key-value pairs
        data_dict = {}

        # Parse the CSV content
        csv_data = response.text.splitlines()
        csv_reader = csv.reader(csv_data[6:])

        for row in csv_reader:
            if len(row) >= 3:
                key = row[1].strip()
                value = row[2].strip()
                data_dict[key] = value

        # Print the key-value pairs
        # for key, value in data_dict.items():
        #     print(f"{key}: {value}")
        return data_dict
    else:
        print("Failed to retrieve data from the URL.")



def get_index_data():

    nse_dict = get_fno_lot_size()

    params = {
        'index': 'NIFTY 50'
    }

    response = session.get(index_url,params=params, headers = head)

    if response.status_code == 200:
        index_data = response.json()['data'];
        for data in index_data:
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


