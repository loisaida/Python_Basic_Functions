import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
from pylab import rcParams
import pandas_datareader.data as pdr
import yfinance as yf
import warnings
from bs4 import BeautifulSoup as soup
from urllib.request import Request, urlopen
warnings.filterwarnings('ignore')
yf.pdr_override()

start = dt.date(2006, 1, 1)
ticker = "SPY"

naaim_url = 'https://www.naaim.org/programs/naaim-exposure-index/'
req = Request(naaim_url, headers={'User-Agent': 'Mozilla/5.0'})
webpage = urlopen(req).read()
html = soup(webpage, "html.parser")
a_tags = html.find_all('a')
excel_url = a_tags[53]['href']

data = pd.read_excel(excel_url)
data = data.set_index('Date')
data = data.iloc[::-1]
data = data.truncate(before=start)

df = data[["NAAIM Number"]]
df.columns = ["NAAIM"]
df[f"{ticker} Price"] = pdr.get_data_yahoo(ticker, start)["Adj Close"]

df['label'] = 'rangebound'
df.loc[(df['NAAIM']) > 85, 'label'] = 'NAAIM > 80'
df.loc[(df['NAAIM']) >= 90, 'label'] = 'NAAIM >= 90'
df.loc[(df['NAAIM']) < 30, 'label'] = 'NAAIM < 30'
df.loc[(df['NAAIM']) < 10, 'label'] = 'NAAIM < 10'

label2color = {
    'NAAIM >= 90': 'red',
    'NAAIM > 80': 'yellow',
    'rangebound': 'blue',
    'NAAIM < 30': 'springgreen',
    'NAAIM < 10': 'green',
}
df['color'] = df['label'].apply(lambda label: label2color[label])

fig, ax = plt.subplots()

def gen_repeating(s):
    i = 0
    while i < len(s):
        j = i
        while j < len(s) and s[j] == s[i]:
            j += 1
        yield (s[i], i, j-1)
        i = j

for color, start, end in gen_repeating(df['color']):
    if start > 0:
        start -= 1
    idx = df.index[start:end+1]
    df.loc[idx, f"{ticker} Price"].plot(ax=ax, color=color, label='', title=f"NAAIM Exposure Index on {ticker} Price")

handles, labels = ax.get_legend_handles_labels()

r_line = plt.Line2D((0,1),(0,0), color='red')
y_line = plt.Line2D((0,1),(0,0), color='yellow')
bl_line = plt.Line2D((0,1),(0,0), color='blue')
b_line = plt.Line2D((0,1),(0,0), color='springgreen')
g_line = plt.Line2D((0,1),(0,0), color='green')

ax.legend(
    handles + [r_line, y_line, bl_line, b_line, g_line],
    labels + [
        'NAAIM >= 90',
        'NAAIM > 80',
        '30 < NAAIM < 80',
        'NAAIM < 30',
        'NAAIM < 10',
    ],
    loc='best',
)

rcParams['figure.figsize'] = 15,10
plt.show()