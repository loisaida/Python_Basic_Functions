import os
import smtplib
from email.message import EmailMessage
import yfinance as yf
import datetime as dt
import pandas as pd
from pandas_datareader import data as pdr
import time

EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')
msg = EmailMessage()

yf.pdr_override()
start = dt.date.today() - dt.timedelta(days = int(365))
end = dt.date.today()

stock = "TSLA"
TargetPrice = 900

msg['Subject'] = f'Alert on {stock}!'
msg['From'] = ''
msg['To'] = ''

alerted=False

while True:
	df = pdr.get_data_yahoo(stock, start, end)
	currentClose=df["Adj Close"][-1]

	condition=currentClose > TargetPrice

	if(condition and alerted==False):
		alerted=True

		message=stock +" Has activated the alert price of "+ str(TargetPrice) +\
		 "\nCurrent Price: "+ str(currentClose)

		print(message)
		msg.set_content(message)

		files=[r""]
		for file in files:
			with open(file,'rb') as f:
				file_data=f.read()
				file_name=""

				msg.add_attachment(file_data, maintype="application",
					subtype='ocetet-stream', filename=file_name)

		with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
		    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
		    smtp.send_message(msg)
		    print("completed")
			
	else:
		print("No new alerts")
	
	time.sleep(60)
