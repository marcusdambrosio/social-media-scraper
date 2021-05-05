import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA
from matplotlib import style
# style.use('ggplot')
import os
import datetime as dt
import sys
plt.rcParams['font.size'] = 35

possibleSubs = ['posts', 'cryptocurrency', 'investing', 'wallstreetbets', 'master']

def post_frequency(fi, subreddit, volume = False, show = True, save = False):
    file = [c for c in os.listdir('DATA') if fi in c and subreddit in c]
    data = pd.read_csv(os.path.join('DATA', file[0]))
    postDates = []
    dayAgg = []
    for date, dat in data.groupby('date'):
        postDates.append(date), dayAgg.append(len(dat))

    postDates = [dt.datetime.strptime('2021-'+d, '%Y-%m-%d') for d in postDates]
    priceData = pd.read_csv('PRICEDATA/dogePriceData.csv', index_col='Date', parse_dates=True)
    priceDates = [d.strftime('%m-%d') for d in priceData.index]
    priceDates = [dt.datetime.strptime('2021-'+d, '%Y-%m-%d') for d in priceDates]

    fig,ax = plt.subplots(figsize = (28,16))

    ax.plot(postDates, dayAgg, color = 'Red', linewidth=2, label = 'posts')
    ax.set_xlabel("Date",labelpad=20)
    ax.set_ylabel("Number of Mentions", color="red",labelpad=20)
    ax.set_xlim(postDates[0], postDates[-1])
    ax.tick_params(rotation = 45)

    ax2 = ax.twinx()
    ax2.plot(priceDates, priceData['Close'], linewidth=2, color = 'green', label = 'price')
    ax2.set_ylabel('Dogecoin Price (USD)',  color = 'green', labelpad=20)

    if volume:
        ax3 = ax.twinx()
        ax3.spines['right'].set_position(('axes', 1.12))
        ax3.bar(priceDates, priceData['Volume']/1e10, color = 'blue', alpha = .2)
        ax3.set_ylabel('Volume (1e10)', color='blue', alpha = .5, labelpad=20)
    fig.tight_layout()

    if show:
        if save:
            if volume:
                plt.savefig(f'GRAPHS\FREQUENCY\WITHVOLUME\{fi}_{subreddit}_withvol_graph.png')
                plt.show()
            else:
                plt.savefig(f'GRAPHS\FREQUENCY\{fi}_{subreddit}_graph.png')
                plt.show()
        else:
            plt.show()
    else:
        if save:
            if volume:
                plt.savefig(f'GRAPHS\FREQUENCY\WITHVOLUME\{fi}_{subreddit}_withvol_graph.png')
            else:
                plt.savefig(f'GRAPHS\FREQUENCY\{fi}_{subreddit}_graph.png')
        else:
            print('Nothing displayed or saved.')

'''example displaying a combination of all subreddits (master) with volume bars included'''
# post_frequency('dogecoin', 'master', volume = True, show = True, save = False)

'''generating and saving plots for every subreddit with and without volume'''
for sub in possibleSubs:
    for volBool in [True, False]:
        post_frequency('dogecoin', sub, volume = volBool, show = False, save = True)

def all_subs(fi, volume = False, show = True, save = False):
    fig,ax = plt.subplots(figsize = (28,20))
    ax2 = ax.twinx()
    subLabels = ['Dogecoin', 'Cryptocurrency', 'Investing', 'Wallstreetbets']
    colors = ['red', 'darkcyan', 'purple', 'darkblue']
    for i, subreddit in enumerate(['posts', 'cryptocurrency', 'investing', 'wallstreetbets']):
        data = pd.read_csv(f'DATA\{fi}_{subreddit}.csv')
        postDates = []
        dayAgg = []
        for date, dat in data.groupby('date'):
            postDates.append(date), dayAgg.append(len(dat))
        postDates = [dt.datetime.strptime('2021-' + d, '%Y-%m-%d') for d in postDates]
        ax.plot(postDates,dayAgg, linewidth = 2, color= colors[i], label=subLabels[i])

    priceData = pd.read_csv('PRICEDATA/dogePriceData.csv', index_col='Date', parse_dates=True)
    priceDates = [d.strftime('%m-%d') for d in priceData.index]
    priceDates = [dt.datetime.strptime('2021-'+d, '%Y-%m-%d') for d in priceDates]

    ax.set_xlabel("Date",labelpad=12)
    ax.set_ylabel("Number of Mentions",labelpad=12)
    ax.set_xlim(priceDates[0], priceDates[-1])
    ax.tick_params(rotation=45)
    ax.legend(loc='upper left')

    ax2.plot(priceDates, priceData['Close'], color = 'green')
    ax2.set_ylabel('Dogecoin Price (USD)', color = 'green', labelpad=12)
    fig.tight_layout()

    if volume:
        print('This function is not yet set up to display volume.')
        volume = False
    if show:
        if save:
            if volume:
                plt.savefig(f'GRAPHS\FREQUENCY\WITHVOLUME\{fi}_allsubs_withvol_graph.png')
                plt.show()
            else:
                plt.savefig(f'GRAPHS\FREQUENCY\{fi}_allsubs_graph.png')
                plt.show()
        else:
            plt.show()
    else:
        if save:
            if volume:
                plt.savefig(f'GRAPHS\FREQUENCY\WITHVOLUME\{fi}_allsubs_withvol_graph.png')
            else:
                plt.savefig(f'GRAPHS\FREQUENCY\{fi}_allsubs_graph.png')
        else:
            print('Nothing displayed or saved.')

'''example displaying graph with each individual subreddit as its own line superimposed on one plot'''
# all_subs('dogecoin', volume = True, show = True, save = False)
