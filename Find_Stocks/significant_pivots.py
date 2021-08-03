import datetime as dt
import pandas as pd
from pandas_datareader import DataReader
import yahoo_fin.stock_info as si
from pandas_datareader import data as pdr

num_of_years = 5
start = dt.date.today() - dt.timedelta(days = int(365.25*num_of_years))
end = dt.date.today()

tickers = si.tickers_sp500()
tickers = [item.replace(".", "-") for item in tickers]

close_glv_percentage = []
close_glv_tickers = []

for ticker in tickers:
    try:
        print (ticker+':')
        price = si.get_live_price(ticker)
        
        df = pdr.get_data_yahoo(ticker, start, end)
        df.drop(df[df["Volume"]<1000].index, inplace=True)
        
        dfmonth=df.groupby(pd.Grouper(freq="M"))["High"].max()
        
        glDate=0
        lastGLV=0
        currentDate=""
        curentGLV=0
        for index, value in dfmonth.items():
          if value > curentGLV:
            curentGLV=value
            currentDate=index
            counter=0
          if value < curentGLV:
            counter=counter+1
        
            if counter==3 and ((index.month != end.month) or (index.year != end.year)):
                if curentGLV != lastGLV:
                    pass
                glDate=currentDate
                lastGLV=curentGLV
                counter=0
        
        if lastGLV==0:
            message = f"{ticker} has not formed a green line yet"
        
        else:
            if lastGLV < 1.05 * price and lastGLV > .95*price:
                diff = lastGLV/price
                diff = round(diff - 1, 3)
                diff = diff*100
                
                print (f"\n{ticker.upper()}'s last green line value ({round(lastGLV, 2)}) is {round(diff,1)}% greater than it's current price ({round(price, 2)})")
                message=("Last Green Line: "+str(round(lastGLV, 2))+" on "+str(glDate.strftime('%Y-%m-%d')))
    
                close_glv_tickers.append(ticker)
                close_glv_percentage.append(diff)
            
            else:
                diff = lastGLV/price
                diff = round(diff - 1, 3)
                diff = diff*100
                message=(f"Last Green Line for {ticker}: "+str(round(lastGLV, 2))+" on "+str(glDate.strftime('%Y-%m-%d')))
    
        print(message)
        print('-'*100)
    except Exception as e:
        print (e)
        pass

df = pd.DataFrame(list(zip(close_glv_tickers, close_glv_percentage)), columns =['Ticker', 'Percentage from GLV'])
df = df.reindex(df["Percentage from GLV"].abs().sort_values().index)

df.to_csv(f'green_line_{[dt.datetime.today()][0]}.csv', index=False)

print ('Watchlist: ')
print (df)
