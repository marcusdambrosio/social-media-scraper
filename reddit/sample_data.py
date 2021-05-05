import pandas as pd

dogeData = pd.read_csv('DATA/dogecoin_posts.csv')
dogeMentions = pd.read_csv('DATA/dogecoin_in_cryptocurrency.csv')

print(dogeData.columns)

for col in dogeData.columns:
    print(col , ': ', dogeData.loc[0, col])





