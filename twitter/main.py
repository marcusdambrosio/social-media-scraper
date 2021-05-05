import config
import tweepy
import pickle
import pandas as pd
import inspect
import datetime as dt
import time
auth = tweepy.OAuthHandler(config.APIKEY, config.API_SECRET)
auth.set_access_token(config.ACCESS, config.ACCESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)


KEYWORD = 'doge'
count = 50000 #max number of tweets
keys = ['time', 'text', 'user','retweets', 'favorites', 'hashtags', 'screenname', 'followers', 'friends', 'accountFavorites']
# startDate = dt.datetime(2021, 1,15,12,00,00)
def main():
    tic = dt.datetime.today()
    tweets = tweepy.Cursor(api.search, q = KEYWORD).items(count)
    counter = 0
    tweetData = {}
    while True:
        try:
            tweet = tweets.next()
            counter += 1
            if counter%1000 == 0:
                print(dt.datetime.today() - tic, ' since last 1000 tweets')
                tic = dt.datetime.today()


            for i, dat in enumerate([tweet.created_at, tweet.text, tweet.user, tweet.retweet_count, tweet.favorite_count, tweet.entities['hashtags']]):

                if keys[i] == 'user':
                    for i, userDat in enumerate([dat._json['screen_name'], dat._json['followers_count'],dat._json['friends_count'],dat._json['favourites_count']]):
                        if keys[i+6] not in tweetData.keys():
                            tweetData[keys[i+6]] = [userDat]
                        else:
                            tweetData[keys[i+6]].append(userDat)

                else:
                    if keys[i] == 'hashtags':
                        dat = [c['text'] for c in dat]
                    if keys[i] not in tweetData.keys():
                        tweetData[keys[i]] = [dat]
                    else:
                        tweetData[keys[i]].append(dat)
        except tweepy.TweepError:
            print('hit rate limit')
            time.sleep(60*15)
            continue
        except StopIteration:
            print('process completed.')
            break

    return tweetData
#
# if __name__ == '__main__':
#     tweetDict = main()
#     tweetDF = pd.DataFrame.from_dict(tweetDict, orient='columns')
#     tweetDF.to_csv(f'DATA\{KEYWORD}_on_twitter.csv', index=False)



