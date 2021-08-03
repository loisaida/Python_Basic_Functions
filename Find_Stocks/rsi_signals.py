import datetime
import talib
from pandas_datareader import data as pdr
import pandas as pd
import yahoo_fin.stock_info as si

start_date = datetime.datetime.now() - datetime.timedelta(days=365)
end_date = datetime.date.today()
tickers = si.tickers_sp500()
tickers = [item.replace(".", "-") for item in tickers]

oversold = []
overbought = []

for ticker in tickers:
    try:
        data = pdr.get_data_yahoo(ticker, start_date, end_date)
        data["rsi"] = talib.RSI(data["Close"])
        rsi = data["rsi"][-1]
        print ('\n{} has an rsi value of {}'.format(ticker, round(rsi, 2)))
        
        if rsi <= 30:
            oversold.append(ticker)
            
        elif rsi >= 70:
            overbought.append(ticker)

    except Exception as e:
        print (e)
        continue

print (oversold)
print (overbought)
