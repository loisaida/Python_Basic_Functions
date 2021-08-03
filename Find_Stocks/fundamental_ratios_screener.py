import requests
import pandas as pd
from config import financial_model_prep

demo = financial_model_prep()
url = (f'https://financialmodelingprep.com/api/v3/stock-screener?marketCapMoreThan=1000000000&betaMoreThan=1&volumeMoreThan=10000&sector=Technology&exchange=NASDAQ&dividendMoreThan=0&limit=1000&apikey={demo}')

companies = []
screener = requests.get(url).json()
for item in screener:
    companies.append(item['symbol'])

value_ratios ={}
count = 0
for company in companies:
    try:
        if count < 30:
            count = count + 1
            fin_ratios = requests.get(f'https://financialmodelingprep.com/api/v3/ratios/{company}?apikey={demo}').json()
            value_ratios[company] = {}
            value_ratios[company]['ROE'] = fin_ratios[0]['returnOnEquity']
            value_ratios[company]['ROA'] = fin_ratios[0]['returnOnAssets']
            value_ratios[company]['Debt_Ratio'] = fin_ratios[0]['debtRatio']
            value_ratios[company]['Interest_Coverage'] = fin_ratios[0]['interestCoverage']
            value_ratios[company]['Payout_Ratio'] = fin_ratios[0]['payoutRatio']
            value_ratios[company]['Dividend_Payout_Ratio'] = fin_ratios[0]['dividendPayoutRatio']
            value_ratios[company]['PB'] = fin_ratios[0]['priceToBookRatio']
            value_ratios[company]['PS'] = fin_ratios[0]['priceToSalesRatio']
            value_ratios[company]['PE'] = fin_ratios[0]['priceEarningsRatio']
            value_ratios[company]['Dividend_Yield'] = fin_ratios[0]['dividendYield']
            value_ratios[company]['Gross_Profit_Margin'] = fin_ratios[0]['grossProfitMargin']
            
            #more financials on growth:https://financialmodelingprep.com/api/v3/financial-growth/AAPL?apikey=demo
            growth_ratios = requests.get(f'https://financialmodelingprep.com/api/v3/financial-growth/{company}?apikey={demo}').json()
            value_ratios[company]['Revenue_Growth'] = growth_ratios[0]['revenueGrowth']
            value_ratios[company]['NetIncome_Growth'] = growth_ratios[0]['netIncomeGrowth']
            value_ratios[company]['EPS_Growth'] = growth_ratios[0]['epsgrowth']
            value_ratios[company]['RD_Growth'] = growth_ratios[0]['rdexpenseGrowth']
    except:
        pass

print (value_ratios)

dataframe = pd.DataFrame.from_dict(value_ratios,orient='index')
print(dataframe.head)

ROE = 1.2
ROA = 1.1
Debt_Ratio = -1.1
Interest_Coverage = 1.05
Dividend_Payout_Ratio = 1.01
PB = -1.10
PS = -1.05
Revenue_Growth = 1.25
Net_Income_Growth = 1.10

ratios_mean = []
for item in dataframe.columns:
    ratios_mean.append(dataframe[item].mean())

dataframe = dataframe / ratios_mean
dataframe['ranking'] = dataframe['NetIncome_Growth']*Net_Income_Growth + dataframe['Revenue_Growth']*Revenue_Growth  + dataframe['ROE']*ROE + dataframe['ROA']*ROA + dataframe['Debt_Ratio'] * Debt_Ratio + dataframe['Interest_Coverage'] * Interest_Coverage + dataframe['Dividend_Payout_Ratio'] * Dividend_Payout_Ratio + dataframe['PB']*PB + dataframe['PS']*PS

print(dataframe.sort_values(by=['ranking'],ascending=False))