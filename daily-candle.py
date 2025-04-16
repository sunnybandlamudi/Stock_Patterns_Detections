import yfinance as yf
import pandas as pd

# Settings
ticker = "NIFTYBEES.NS"
period = "1y"
interval = "1d"
units_per_red_candle = 2

# Fetch data
data = yf.download(ticker, start='2023-01-01',period=period, interval=interval)
# Remove any rows with missing Close or Open values
data = data.dropna(axis=1)


# Identify red candles
data['RedCandle'] = data['Close'] < data['Open']



# Buy 2 whole units on red candle days
data['UnitsBought'] = data['RedCandle'].apply(lambda x: units_per_red_candle if x else 0)


# Calculate investment per day
data['Investment'] = data['UnitsBought'] * data['Close'].squeeze()
# Cumulative investment and units
data['TotalInvestment'] = data['Investment'].cumsum()
data['TotalUnits'] = data['UnitsBought'].cumsum()


# Portfolio value = total units × current price
data['PortfolioValue'] = data['TotalUnits'] * data['Close'].squeeze()

# print(data.tail())

# Results
total_invested = data['TotalInvestment'].iloc[-1]
final_portfolio_value = data['PortfolioValue'].iloc[-1]
profit = final_portfolio_value - total_invested

print(f"Red Candle Days: {(data['RedCandle'] == True).sum()}")
print(f"Green Candle Days: {(data['RedCandle'] == False).sum()}")
print(f"Total Trading Days: {len(data)}")
print("---------------------------------------")
print(f"Total Invested: ₹{total_invested:.2f}")
print(f"Portfolio Value: ₹{final_portfolio_value:.2f}")
print(f"Profit/Loss: ₹{profit:.2f}")
print(f"ROI: {(profit*100)/total_invested:.2f}%")
