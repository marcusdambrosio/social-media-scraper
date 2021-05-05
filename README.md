# FINAN5530_Final

### 5530 Final Project Code for James Bullock, Marcus D'Ambrosio, Kelsey Heffernan, Devin Valiquett

This collection of code will pull reddit and twitter data when given keywords and/or subreddits to search. Additionally, it contains a lot of data visualization code and the results of this data vis in the "GRAPHS" folders. The actual reddit data that was pulled for use was too big to upload to github so it may be found here:
https://drive.google.com/drive/folders/1l7mxcP6thN5dBGzuBzgHJPsD4lQuBszn?usp=sharing

A lot of this is unoptimized and undocumented spaghetti code but it got the job done and I do not have it in me to fix everything up since this was the very last think I had to do before graduating.

Here is a brief guide to the contents:<br>
\reddit, \twitter --> parent folders for the respective data sources <br>
\reddit\GRAPHS, \twitter\GRAPHS --> holds .png files for graphical data that we generated <br>
\reddit\PRICEDATA, \twitter\PRICEDATA --> holds dogecoin price data<br>
\reddit\CORR --> holds correlation tables for reddit data<br>
\reddit\get_price_data --> pulls data for whatever ticker and timeframe you need, saving to \reddit\PRICEDATA<br>
\reddit\doge_scrape, \reddit\subreddit_scrape --> pulls reddit posts for dogecoin subreddit or other subreddits <br>
\reddit\data_aggregation --> functions to combine data and stuff <br>
\reddit\frequency_analysis, \reddit\language_analysis --? post frequency and keyword / sentiment analysis functions<br>
\twitter\main --> main file to pull tweets, later found out that this is useless because limiter is so low<br>
\twitter\celebrity_tweets --> visualization for celeb tweets effects on price and volume movement 

Hope you enjoy the project,

Marcus, James, Kelsey, and Devin
