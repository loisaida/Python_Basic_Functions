import pandas as pd
from bs4 import BeautifulSoup as soup
from urllib.request import Request, urlopen
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

finviz_url = 'https://finviz.com/screener.ashx?v=151&f=cap_smallover,fa_epsqoq_o20,fa_epsyoy_o20,fa_epsyoy1_pos,fa_grossmargin_pos,fa_roe_pos,fa_salesqoq_o20,sh_avgvol_o200,sh_price_o10,ta_sma20_pa,ta_sma200_pa,ta_sma50_pa&ft=4&o=-high52w&ar=180'
num_of_stocks = 100

frames = []
for i in range(1, num_of_stocks+1, 20):
    url = (f"{finviz_url}&r={i}")
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    html = soup(webpage, "html.parser")

    stocks = pd.read_html(str(html))[-2]
    stocks.columns = stocks.iloc[0]
    stocks = stocks[1:]
    stocks = stocks.set_index('Ticker')
    frames.append(stocks)

df = pd.concat(frames)
df = df.drop_duplicates()
df = df.drop(columns = ['No.'])
tickers = df.index

print ('\nGrowth Stocks Screener: ')
print (df)

print ('\nList of Stocks: : ')
print (*tickers, sep =', ')
