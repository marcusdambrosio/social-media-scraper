import pandas_datareader as web
import datetime as dt

def pull_data(ticker, startDate, endDate):
    '''PULL DATA FROM YAHOO FINANCE AND SAVE IN PRICEDATA FOLDER'''
    data = web.DataReader(ticker, 'yahoo', startDate, endDate)
    if type(endDate) != str: endDate = endDate.strftime("%m-%d-%Y")
    data.to_csv(f'PRICEDATA\{ticker}_{startDate.replace("-", "")}-{endDate.replace("-","")}.csv')

# pull_data('DOGE-USD', '01-01-2019', '05-03-2021')
