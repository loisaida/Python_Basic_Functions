import yfinance as yf
import datetime as dt
from pandas_datareader import data as pdr
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as mticker
yf.pdr_override()

sma = 50
limit = 30
num_days = 100

start = dt.date(1980,1,1)
end = dt.date.today()

ticker = input("Enter the ticker symbol: ")

while ticker != "quit":
    df = pdr.get_data_yahoo(ticker, start, end)

    df['SMA'+str(sma)] = df["Adj Close"].rolling(window=sma).mean()
    df['PC'] = ((df["Adj Close"]/df['SMA'+str(sma)])-1)*100

    mean =df["PC"].mean()
    stdev=df["PC"].std()
    current=df["PC"][-1]
    yday=df["PC"][-2]

    print(f"Current % Away from {sma}SMA: {current}")
    print(f"Mean: {mean}")
    print(f"Standard Dev: {stdev}")

    bins = np.arange(-100, 100, 1)

    fig, ax1 = plt.subplots()
    plt.xlim([df["PC"].min()-5, df["PC"].max()+5])
    plt.hist(df["PC"], bins=bins, alpha=0.5)
    plt.title(ticker+"-- % From "+str(sma)+" SMA Histogram since "+str(start.year))
    plt.xlabel('Percent from '+str(sma)+' SMA (bin size = 1)')
    plt.ylabel('Count')
    plt.axvline(x=mean, ymin=0, ymax=1, color='k', linestyle='--')
    plt.axvline(x=stdev+mean, ymin=0, ymax=1, color='gray', alpha=1, linestyle='--')
    plt.axvline(x=2*stdev+mean, ymin=0, ymax=1, color='gray',alpha=.75, linestyle='--')
    plt.axvline(x=3*stdev+mean, ymin=0, ymax=1, color='gray', alpha=.5, linestyle='--')
    plt.axvline(x=-stdev+mean, ymin=0, ymax=1, color='gray', alpha=1, linestyle='--')
    plt.axvline(x=-2*stdev+mean, ymin=0, ymax=1, color='gray',alpha=.75, linestyle='--')
    plt.axvline(x=-3*stdev+mean, ymin=0, ymax=1, color='gray', alpha=.5, linestyle='--')
    plt.axvline(x=current, ymin=0, ymax=1, color='r', label='Current Deviation')
    plt.axvline(x=yday, ymin=0, ymax=1, color='blue', label='Yesterday\'s Deviation')
    plt.legend()
    ax1.xaxis.set_major_locator(mticker.MaxNLocator(14))

    fig2, ax2 = plt.subplots()
    df=df[-num_days+50:]
    df['PC'].plot(label=f'Percent from {sma}SMA', color='k')
    plt.title(f"{ticker} % from {sma}SMA over last {num_days} days")
    plt.xlabel('Date')
    plt.ylabel(f'Percent from {sma}SMA')
    ax2.xaxis.set_major_locator(mticker.MaxNLocator(8))
    plt.axhline(y=limit, xmin=0, xmax=1, color='r', label='Warning % Deviation')
    plt.legend()
    plt.show()

    ticker = input("Enter the ticker symbol: ")