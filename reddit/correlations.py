import pandas as pd
import numpy as np
import os
import sys
import datetime as dt
from tabulate import tabulate

possibleSubs = ['posts', 'cryptocurrency', 'investing', 'wallstreetbets', 'master']
def print_corrs(fi, subreddit, corrType = 'frequency', langType = 'both'):
    subKeys = {'posts':'Dogecoin',
               'investing':'Investing',
               'cryptocurrency':'Cryptocurrency',
               'wallstreetbets':'Wallstreetbets',
               'master': 'All Subreddits'}

    allSubs = pd.DataFrame()
    if type(subreddit) != str:
        for sub in subreddit:
            if corrType == 'language':
                data = pd.read_csv(os.path.join('DATA', f'{corrType}\{fi}_{sub}_{langType}.csv'))
            else:
                data = pd.read_csv(os.path.join('DATA', f'{corrType}\{fi}_{sub}.csv'))
            postDates = []
            dayAgg = []
            for date, dat in data.groupby('date'):
                postDates.append(date), dayAgg.append(len(dat))
            postDates = [dt.datetime.strptime('2021-' + d, '%Y-%m-%d') for d in postDates]
            allSubs = allSubs.append({'sub': sub,'postDates':postDates, 'dayAgg':dayAgg}, ignore_index=True)
    else:
        if corrType == 'language':
            data = pd.read_csv(os.path.join('DATA', f'{corrType}\{fi}_{subreddit}_{langType}.csv'))
        else:
            data = pd.read_csv(os.path.join('DATA', f'{corrType}\{fi}_{subreddit}.csv'))
        postDates = []
        dayAgg = []
        for date, dat in data.groupby('date'):
            postDates.append(date), dayAgg.append(len(dat))
        postDates = [dt.datetime.strptime('2021-'+d, '%Y-%m-%d') for d in postDates]

    priceData = pd.read_csv('PRICEDATA/DOGE-USD_01012021-05042021.csv', index_col='Date', parse_dates=True)
    allDat = []

    for i in priceData.index:
        if i in allDat:
            priceData.drop(i, inplace = True)
        else:
            allDat.append(i)

    if len(allSubs):
        corrDf = pd.DataFrame(columns=[subKeys[s] for s in subreddit], index=['Close', 'Volume'])
        for sub in subreddit:
            # tempPostDates = [d for d in allSubs[sub][0] if d in priceData.index]
            # tempPostDates = set(allSubs[sub][0]).intersection(priceData.index)
            subDf = allSubs[allSubs['sub'] == sub]
            tempDf = pd.DataFrame()
            tempDf['dayAgg'], tempDf['postDates'] = subDf['dayAgg'].tolist()[0], subDf['postDates'].tolist()[0]
            tempPostDates = []
            tempPostInd = []
            for date in pd.Series(tempDf['postDates'].tolist() + priceData.index.tolist()).unique():
                if date in tempDf['postDates'].tolist() and date in priceData.index.tolist():
                    tempPostDates.append(date)
                    tempPostInd.append(tempDf[tempDf['postDates'] == date].index[0])

            tempDf = tempDf.loc[tempPostInd, :]
            tempPriceData = priceData.loc[tempPostDates, :]

            corrDf.loc['Close',subKeys[sub]] = np.corrcoef(tempDf['dayAgg'][:-1], tempPriceData['Close'].shift(-1)[:-1])[0][-1]
            corrDf.loc['Volume',subKeys[sub]] = np.corrcoef(tempDf['dayAgg'][:-1], tempPriceData['Volume'].shift(-1)[:-1])[0][-1]
    else:
        postDates = [d for d in postDates if d in priceData.index]
        priceData = priceData.loc[postDates, :]
        corrDf = pd.DataFrame(columns=[subKeys[subreddit]], index=['Close', 'Volume'])
        corrDf.loc['Close', subKeys[subreddit]] = np.corrcoef(dayAgg[:-1], priceData['Close'].shift(-1)[:-1])[0][-1]
        corrDf.loc['Volume', subKeys[subreddit]] = np.corrcoef(dayAgg[:-1], priceData['Volume'].shift(-1)[:-1])[0][-1]

    print(tabulate(corrDf, headers= corrDf.columns))


print_corrs('dogecoin', possibleSubs, corrType = 'language', langType = 'both')
# print_corrs('dogecoin', 'master')
