import pandas as pd
import datetime as dt

data = pd.read_csv('DATA/dogecoin_posts.csv')

times = data['time'].tolist()

t1, t2 = times[0], times[-1]

print(len(data))
for t in [t1, t2]:
    print(dt.datetime.utcfromtimestamp(t))