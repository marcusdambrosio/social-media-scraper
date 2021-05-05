import numpy as np
import pandas as pd
from os import path

import self as self
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt

df = pd.read_csv("dogecoin_posts.csv")

print(df)


# print(dogeCoin)

# def transform_format(val):
#     if val == 0:
#         return 255
#     else:
#         return val
#
#
# transformedDogeCoin = np.ndarray((dogeCoin.shape[0], dogeCoin.shape[1]), np.int32)
#
# for i in range(len(dogeCoin)):
#     transformedDogeCoin[i] = list(map(transform_format(all), dogeCoin[i]))
#
# print(transformedDogeCoin)



dogeCoinIcon = np.array(Image.open("Dogecoin-icon.png"))

text = ",".join(map(str, df.title))

stopWords = set(STOPWORDS)
stopWords.update(["don't", "today", "got", "guy", "guys", "Let's", "Let", "will", "s", "u", "don", "t"])

wordcloud = WordCloud(stopwords=stopWords, background_color="black", mode="RGBA", max_words=15000, mask=dogeCoinIcon)
wordcloud.generate(text)
image_colors = ImageColorGenerator(dogeCoinIcon)
plt.figure(figsize=[10,5])
plt.imshow(wordcloud.recolor(color_func=image_colors), interpolation="bilinear")
plt.axis("off")
plt.show()



# RedditLogo = np.array(Image.open("RedditLogo.png"))
#
# textTwo = ",".join(map(str, df.body))
#
# stopWords = set(STOPWORDS)
# stopWords.update(["don't", "today", "got", "guy", "guys", "Let's", "Let", "will", "s", "u", "don", "t", "removed", "nan", "nan nan", "nan deleted", "nan removed", "removed nan", "deleted nan", "deleted", "deleted deleted"])
#
# wordcloudTwo = WordCloud(stopwords=stopWords,background_color="white", mode="RGBA", max_words=1000, mask=RedditLogo)
# wordcloudTwo.generate(textTwo)
# image_colors = ImageColorGenerator(RedditLogo)
# plt.figure(figsize=[10,5])
# plt.imshow(wordcloudTwo.recolor(color_func=image_colors), interpolation="bilinear")
# plt.axis("off")
# plt.show()

