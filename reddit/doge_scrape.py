import praw
import pandas as pd
import datetime as dt
import config
from psaw import PushshiftAPI

reddit = praw.Reddit(client_id=config.client, client_secret=config.secret, user_agent=config.user)
api = PushshiftAPI(reddit)

subreddits = ['dogecoin', 'investing', 'bitcoin', 'cryptocurrency', 'wallstreetbets', 'all']
subreddits = ['dogecoin']

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


    for key, dat in data.items():
        dat.to_csv(key+'_posts.csv', index = False)

# pull_post_data(subreddits)
#
# data = pd.read_csv('dogecoin_posts.csv')
# times = data['time'].tolist()
#
# firstt = times[0]
# lastt = times[-1]
#
# for t in [firstt, lastt]:
#     print(dt.datetime.utcfromtimestamp(t))

tic = dt.datetime.today()

start = int(dt.datetime(2021, 1, 1).timestamp())
start = int(dt.datetime(2021, 4,26).timestamp())
posts = list(api.search_submissions(after = start,
                                 subreddit = 'dogecoin',
                                 filter = ['title', 'selftext', 'created_utc','num_comments','score','permalink','upvote_ratio'],
                                 limit = 1000000,
                                 stop_condition = lambda x: x.created_utc < dt.datetime.now(dt.timezone.utc).replace(tzinfo = dt.timezone.utc).timestamp() - 60*60*24*200))

print(f'the process took {dt.datetime.today() - tic} seconds')


subDF = pd.DataFrame(columns=['title', 'body', 'time', 'numComments', 'score', 'url', 'upvoteRatio'])
times = []
subDict = {}
keys = ['title', 'body', 'time', 'numComments', 'score', 'url', 'upvoteRatio']

counter = 1
tic = dt.datetime.today()
for post in posts:
    if counter%10000 == 0:
        print(f'Time passed since last 10k: {dt.datetime.today() - tic}')
    for i, value in enumerate([post.title,post.selftext, post.created_utc, post.num_comments, post.score, post.permalink, post.upvote_ratio]):
        if keys[i] not in subDict.keys():
            subDict[keys[i]] = [value]
        else:
            subDict[keys[i]].append(value)
    counter += 1

    # subDF = subDF.append({'title': post.title,
    #                       'body': post.selftext,
    #                       'time': post.created_utc,
    #                       'numComments': post.num_comments,
    #                       'score': post.score,
    #                       'url': post.permalink,
    #                       'upvoteRatio': post.upvote_ratio}, ignore_index=True)




subDF = pd.DataFrame.from_dict(subDict, orient = 'columns')
subDF.to_csv('dogecoin_postsNEW.csv', index = False)
