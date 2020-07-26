import pandas as pd
from twitterscraper import query_tweets
import datetime as dt 
import pandas as pd

a = pd.read_csv('handles.csv',skiprows=0)
a = pd.DataFrame(a)

b = ['MKTWeconomics','AnilSinghvi_']
a=a.values.tolist()
for i in a:
    b = b + i
a = pd.read_csv('handles2.csv',skiprows=0)
a = pd.DataFrame(a)
a=a.values.tolist()
for i in a:
    b = b + i
b= list(set(b))

begin_dt = dt.date(2020,4,28)
end_dt   = dt.date(2020,4,29)
limit = 5000
lang = 'english'

terms = ['#nifty','#NIFTY','#MarketLive','#sensex','#SENSEX','#stockmarket']
results = pd.DataFrame(columns=['Time','Username','Tweet'])

for i in range(len(terms)):
    tweets = query_tweets(terms[i], begindate = begin_dt, enddate = end_dt, limit = limit, lang = lang)
    test_df = pd.DataFrame(t.__dict__ for t in tweets)
    twitter_data = test_df.filter(['parent_tweet_id', 
           'screen_name', 'text',  'timestamp',
           'tweet_id',  'user_id', 'username'
           ])
    twitter_data.sort_values("tweet_id", inplace = True)
    twitter_data.drop_duplicates(subset ="tweet_id", keep = False, inplace = True) 
    twitter_data.to_csv(f'data{i}.csv', index = False )

    tweets = pd.read_csv(f'data{i}.csv')
    tweets = pd.DataFrame(tweets)
    tweets = tweets.reset_index()
    for i in range(len(tweets)):
        if tweets.loc[i]['screen_name'] in b:
            results = results.append({'Time':tweets.loc[i]['timestamp'] ,'Username': tweets.loc[i]['username'],'Tweet':tweets.loc[i]['text'] },ignore_index=True)

results.to_csv('twitter_results.csv')


    
