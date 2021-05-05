import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
# style.use('ggplot')
import sys
import os
import math
import datetime as dt
plt.rcParams['font.size'] = 35

possibleSubs = ['posts', 'cryptocurrency', 'investing', 'wallstreetbets', 'master']

def word_in(word, title, body):
    tempTitle = tempBody = temp = 0
    try:
        if word in title and word in body:
            tempTitle, tempBody, temp = 1,1,1
            tempTitle = 1
        elif word in body:
            tempBody = 1
        else:
            # tempBody.append(0), tempTitle.append(0), temp.append(0)
            return 0
    except:
        if word in title:
            tempTitle = 1
        else:
            return 0

    return [tempTitle, tempBody, temp]

def language_analysis(fi, subreddit, volume = False, show = True, save = False):
    data = pd.read_csv(f'DATA\{fi}_{subreddit}.csv')

    goodWords = ['moon', 'hodl', 'hold', 'good',  'buy', 'up', 'buy the dip']
    goodTitle, goodBody, good = [], [], []
    for row in data.iterrows():
        ind, row = row[0], row[-1]
        try:
            title = row['title'].lower()
        except:
            title = row['title']
        try:
            body = row['body'].lower()
        except:
            body = row['body']
        #check nan
        currTitle = currBody = curr = 0
        for word in goodWords:
            tempTitle = tempBody = temp = 0
            try:
                tempTitle, tempBody, temp = word_in(word, title, body)
                if [tempTitle, tempBody, temp] != [currTitle, currBody, curr]:
                    currTitle, currBody, curr = max(currTitle,tempTitle), max(currBody,tempBody), max(curr,temp)
            except:
                continue

        goodTitle.append(currTitle), goodBody.append(currBody), good.append(curr)
    data['goodTitle'], data['goodBody'], data['good'] = goodTitle, goodBody, good
    data.to_csv(f'DATA\{fi}_{subreddit}.csv')

'''regenerates dataframe with boolean columns indicating whether the title, body, or both of the post had a 'good' sentiment'''
# language_analysis('dogecoin', 'master')

def separate_language_data(fi, subreddit):
    data = pd.read_csv(f'DATA\FREQUENCY\{fi}_{subreddit}.csv')
    goodTitle = data[data['goodTitle'] == 1]
    goodBody = data[data['goodBody'] == 1]
    good = data[data['good'] == 1]
    goodTitle.to_csv(f'DATA\LANGUAGE\{fi}_{subreddit}_title.csv')
    goodBody.to_csv(f'DATA\LANGUAGE\{fi}_{subreddit}_body.csv')
    good.to_csv(f'DATA\LANGUAGE\{fi}_{subreddit}_both.csv')

# for sub in possibleSubs:
#     separate_language_data('dogecoin', sub)

def plot_language(fi, subreddit, volume = False, show = True, save = False):
    data = pd.read_csv(f'DATA\FREQUENCY\{fi}_{subreddit}.csv')
    
    goodTitle = data[data['goodTitle'] == 1]
    goodBody = data[data['goodBody'] == 1]
    good =  data[data['good'] == 1]
    
    labels = ['Title', 'Body', 'Both']
    colors = ['red', 'orange', 'purple']
    fig, ax = plt.subplots(figsize=(28, 16))
    ax2 = ax.twinx()

    for i,d in enumerate([goodTitle, goodBody, good]):
        postDates = []
        dayAgg = []
        for date, dat in d.groupby('date'):
            postDates.append(date), dayAgg.append(len(dat))
        postDates = [dt.datetime.strptime('2021-'+d, '%Y-%m-%d') for d in postDates]
        ax.plot(postDates, dayAgg, linewidth = 2, color = colors[i], label = labels[i])

    priceData = pd.read_csv('PRICEDATA/dogePriceData.csv', index_col='Date', parse_dates=True)
    priceDates = [d.strftime('%m-%d') for d in priceData.index]
    priceDates = [dt.datetime.strptime('2021-' + d, '%Y-%m-%d') for d in priceDates]
    
    ax.set_xlabel("Date", labelpad=20)
    ax.set_ylabel("Number of Posts With \"Positive\" Sentiment", labelpad=20)
    ax.set_xlim(priceDates[0], priceDates[-1])
    ax.tick_params(rotation=45)
    
    ax2.plot(priceDates, priceData['Close'], linewidth = 2, color = 'green')
    ax2.set_ylabel('Dogecoin Price (USD)', color='green', labelpad=20)
    
    if volume:
        ax3 = ax.twinx()
        ax3.spines['right'].set_position(('axes', 1.08))
        ax3.bar(priceDates, priceData['Volume']/1e10, color = 'blue', alpha = .2)
        ax3.set_ylabel('Volume (1e10)', color='blue', alpha = .5, labelpad=20)
        
    ax.legend(loc = 'upper left')
    fig.tight_layout()

    if show:
        if save:
            if volume:
                plt.savefig(f'GRAPHS\LANGUAGE\WITHVOLUME\{fi}_{subreddit}_withvol_language_graph.png')
                plt.show()
            else:
                plt.savefig(f'GRAPHS\LANGUAGE\{fi}_{subreddit}_language_graph.png')
                plt.show()
        else:
            plt.show()
    else:
        if save:
            if volume:
                plt.savefig(f'GRAPHS\LANGUAGE\WITHVOLUME{fi}_{subreddit}_withvol_language_graph.png')
            else:
                plt.savefig(f'GRAPHS\LANGUAGE\{fi}_{subreddit}_language_graph.png')
        else:
            print('Nothing displayed or saved.')

'''generating and saving sentiment plots for every subreddit with and without volume'''
# for sub in possibleSubs:
#     for volBool in [True, False]:
#         plot_language('dogecoin', sub, volume = volBool, show = False, save = True)

plot_language('dogecoin', 'master', volume = False, show = False, save = True)
