import praw
import pandas as pd
import datetime as dt
import config
from psaw import PushshiftAPI
import numpy as np
import time
import sys
reddit = praw.Reddit(client_id=config.client, client_secret=config.secret, user_agent=config.user)
api = PushshiftAPI(reddit)

SUBREDDIT = 'wallstreetbets'
KEYWORD = 'dogecoin'

def pull_post_data(subreddits):
    data = {}
    for sub in subreddits:
        subDF = pd.DataFrame(columns = ['title', 'body', 'time', 'numComments', 'score', 'url', 'upvoteRatio'])
        currSub = reddit.subreddit(sub)
        newPosts = currSub.top('all', limit = 1000000)
        for post in newPosts:
            subDF = subDF.append({'title': post.title,
                                 'body': post.selftext,
                                 'time': post.created_utc,
                                 'numComments': post.num_comments,
                                 'score': post.score,
                                 'url': post.permalink,
                                 'upvoteRatio': post.upvote_ratio}, ignore_index = True)
        data[sub] = subDF

tic = dt.datetime.today()
start = int(dt.datetime(2021, 4, 26).timestamp())
posts = list(api.search_submissions(after = start,
                                 subreddit = SUBREDDIT,
                                 filter = ['title', 'selftext', 'created_utc','num_comments','score','permalink','upvote_ratio'],
                                 limit = 1000000,
                                 q = KEYWORD,
                                 stop_condition = lambda x: x.created_utc < dt.datetime.now(dt.timezone.utc).replace(tzinfo = dt.timezone.utc).timestamp() - 60*60*24*300))


print(f'the process took {dt.datetime.today() - tic} seconds')
print(posts)
try:
    t1, t2 = posts[0].created_utc, posts[-1].created_utc
except:
    print('no new posts')
    sys.exit()


for t in [t1, t2]:
    print(dt.datetime.utcfromtimestamp(t))

subDF = pd.DataFrame(columns=['title', 'body', 'time', 'numComments', 'score', 'url', 'upvoteRatio'])
times = []
subDict = {}
keys = ['title', 'body', 'time', 'numComments', 'score', 'url', 'upvoteRatio']

counter = 1
tic = dt.datetime.today()
for post in posts:
    if counter%10000 == 0:
        print(f'Time passed since last 10k: {dt.datetime.today() - tic}')
    for i, dat in enumerate([post.title,post.selftext, post.created_utc, post.num_comments, post.score, post.permalink, post.upvote_ratio]):
        if keys[i] not in subDict.keys():
            subDict[keys[i]] = [dat]
        else:
            subDict[keys[i]].append(dat)
    counter += 1


subDF = pd.DataFrame.from_dict(subDict, orient = 'columns')
if type(KEYWORD) != str:
    try:
        subDF.to_csv(f'{KEYWORD[0]}_{SUBREDDIT}.csv', index=False)
    except:
        print('LAST SAVE FOR KEYWORDS ', KEYWORD, ' FAILED. SAVED AS TEMP INSTEAD')
        subDF.to_csv(f'temp.csv', index=False)

else:
    subDF.to_csv(f'DATA\{KEYWORD}_in_{SUBREDDIT}NEW.csv', index=False)
