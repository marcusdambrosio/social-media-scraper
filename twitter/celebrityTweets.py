import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates
import datetime as dt
import sys
plt.rcParams['font.size'] = 35
from tabulate import tabulate

possibleCelebs = ['elon' , 'simmons', 'snoop', 'cuban']
celebKeys = {'elon': 'Elon Musk',
             'simmons': 'Gene Simmons',
             'snoop': 'Snoop Dogg',
             'cuban': 'Mark Cuban'}
def tweets_vs_price(celebrity):
    data = pd.read_csv(f'DATA\{celebrity}_tweets.csv', usecols=['Date','Time'])
    DogePrice = pd.read_csv('PRICEDATA\DOGE-USD_01012021-05042021.csv', index_col='Date', parse_dates=True)

    # tweet = CelebrityTweet["Frequency of Tweets"].values
    # price = DogePrice["Adj Close"].values
    # date = DogePrice["Date"].values


    fig, ax = plt.subplots(figsize = (28,16))
    ax2 = ax.twinx()

    dates = []
    aggTweets = []
    for date in data.groupby('Date'):
        dates.append(dt.datetime.strptime(date[0], '%m/%d/%Y')), aggTweets.append(len(date[1]))

    ax.plot(DogePrice.index, DogePrice['Close'], linewidth = 2, color="green")

    ax.set(xlabel="Date", xlim = [DogePrice.index[0], DogePrice.index[-1]], title= f"Dogecoin Price vs. {celebKeys[celebrity]} Tweets")
    ax.set_ylabel( "Dogecoin Price ($)", color = 'green', labelpad=20)
    ax.tick_params(rotation = 45)
    ax2.scatter(dates,aggTweets, s = 400, color= "red")
    ax2.set_ylabel('Number of Tweets', color = 'red', labelpad=20)
    ax2.set_yticks(np.arange(0, max(aggTweets)+2))
    # ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))
    # myFmt = DateFormatter("%m/%d")
    # ax.xaxis.set_major_formatter(myFmt)
    # plt.legend(["Dogecoin Price", "Celebrity Tweet Frequency"])
    # plt.show()
    fig.tight_layout()
    plt.savefig(f'GRAPHS\{celebrity}_tweets')

# for celeb in ['simmons', 'elon', 'snoop', 'cuban']:
#     tweets_vs_price(celeb)


def tweets_vs_priceALL():
    fig, ax = plt.subplots(figsize=(28, 16))
    ax2 = ax.twinx()
    DogePrice = pd.read_csv('PRICEDATA\DOGE-USD_01012021-05042021.csv', index_col='Date', parse_dates=True)

    for celebrity in possibleCelebs:
        data = pd.read_csv(f'DATA\{celebrity}_tweets.csv', usecols=['Date','Time'])
        dates = []
        aggTweets = []
        for date in data.groupby('Date'):
            dates.append(dt.datetime.strptime(date[0], '%m/%d/%Y')), aggTweets.append(len(date[1]))

        ax2.scatter(dates, aggTweets, s=400, color="red")

    ax.plot(DogePrice.index, DogePrice['Close'], linewidth = 2, color="green")
    ax.set(xlabel="Date", xlim = [DogePrice.index[0], DogePrice.index[-1]], title= f"Dogecoin Price vs. All Celebrity Tweets")
    ax.set_ylabel( "Dogecoin Price ($)", color = 'green', labelpad=20)
    ax.tick_params(rotation = 45)
    ax2.set_ylabel('Number of Tweets', color = 'red', labelpad=20)
    ax2.set_yticks(np.arange(0, 9))
    # ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))
    # myFmt = DateFormatter("%m/%d")
    # ax.xaxis.set_major_formatter(myFmt)
    # plt.legend(["Dogecoin Price", "Celebrity Tweet Frequency"])
    fig.tight_layout()


    plt.savefig(f'GRAPHS\ALLCELEB_tweets')

tweets_vs_priceALL()

def tweet_corrs(celebrities):
    
    DogePrice = pd.read_csv('PRICEDATA\DOGE-USD_01012021-05042021.csv', index_col='Date')
    DogePrice['falseInd'] = np.arange(0, len(DogePrice))
    corrDf = pd.DataFrame(columns=[celebKeys[c] for c in celebrities], index=['Close', 'Volume'])
    for celeb in celebrities:
        data = pd.read_csv(f'DATA\{celeb}_tweets.csv', usecols=['Date','Time'])
        dates = []
        aggTweets = []
        tweetData = [0]*len(DogePrice)
        for date in data.groupby('Date'):
            if '2019' in date[0] or '2020' in date[0]:
                continue
            dates.append(dt.datetime.strptime(date[0], '%m/%d/%Y').strftime('%Y-%m-%d')), aggTweets.append(len(date[1]))

        for i, d in enumerate(dates):
            tweetData[int(DogePrice.loc[d, 'falseInd'])] = aggTweets[i]

        tempPrices = DogePrice.loc[dates, :]

        corrDf.loc['Close',celebKeys[celeb]] = np.corrcoef(tweetData[:-1], DogePrice['Close'].shift(-1)[:-1])[0][-1]
        corrDf.loc['Volume',celebKeys[celeb]] = np.corrcoef(tweetData[:-1], DogePrice['Volume'].shift(-1)[:-1])[0][-1]

    print(tabulate(corrDf, headers=corrDf.columns))

# tweet_corrs(possibleCelebs)