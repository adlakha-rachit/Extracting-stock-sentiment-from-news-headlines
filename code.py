from bs4 import BeautifulSoup
import os

html_tables = {}

for table_name in os.listdir('datasets'):
    table_path = f'datasets/{table_name}'
    table_file = open(table_path, 'r')
    html = BeautifulSoup(table_file)
    html_table = html.find(id="news-table")
    html_tables[table_name] = html_table


tsla = html_tables['tsla_22sep.html']
tsla_tr = tsla.findAll('tr')

for i, table_row in enumerate(tsla_tr):
    link_text = table_row.a.get_text()
    data_text = table_row.td.get_text()
    print(f'File number {i+1}:')
    print(link_text)
    print(data_text)
    if i == 3:
        break

parsed_news = []
for file_name, news_table in html_tables.items():
    for x in news_table.findAll('tr'):
        text = x.get_text() 
        headline = x.a.get_text()

        date_scrape = x.td.text.split()
        if len(date_scrape) == 1:
            time = date_scrape[0]
        else:
            date = date_scrape[0]
            time = date_scrape[1]
        ticker = file_name.split('_')[0]
        parsed_news.append([ticker, date, time, headline])

from nltk.sentiment.vader import SentimentIntensityAnalyzer

new_words = {
    'crushes': 10,
    'beats': 5,
    'misses': -5,
    'trouble': -10,
    'falls': -100,
}
vader = SentimentIntensityAnalyzer()
vader.lexicon.update(new_words)


import pandas as pd
columns = ['ticker', 'date', 'time', 'headline']
scored_news =  pd.DataFrame(parsed_news, columns=columns)

scores=[vader.polarity_scores(headline) for headline in scored_news.headline.values]
scores_df = pd.DataFrame(scores)
scored_news = pd.concat([scored_news, scores_df], axis=1)
scored_news['date'] = pd.to_datetime(scored_news.date).dt.date

import matplotlib.pyplot as plt
plt.style.use("fivethirtyeight")
%matplotlib inline

mean_c = scored_news.groupby(['date', 'ticker']).mean()
mean_c = mean_c.unstack(level = 1)
mean_c = mean_c.xs('compound', axis=1)
mean_c.plot.bar()


num_news_before = scored_news['headline'].count()
# Drop duplicates based on ticker and headline
scored_news_clean = scored_news.drop_duplicates(subset=['ticker', 'headline'])
# Count number of headlines after dropping duplicates
num_news_after = scored_news_clean['headline'].count()
# Print before and after numbers to get an idea of how we did 
f"Before we had {num_news_before} headlines, now we have {num_news_after}"

# Set the index to ticker and date
single_day = scored_news_clean.set_index(['ticker', 'date'])
# Cross-section the fb row
single_day = single_day.loc['fb']
# Select the 3rd of January of 2019
single_day = single_day.loc['2019-01-03']
# Convert the datetime string to just the time
single_day['time'] = pd.to_datetime(single_day['time'])
single_day['time'] = single_day.time.dt.time 
 
single_day = single_day.set_index('time')

single_day = single_day.sort_index(ascending = True)

TITLE = "Positive, negative and neutral sentiment for FB on 2019-01-03"
COLORS = ["red","green", "orange"]
# Drop the columns that aren't useful for the plot
plot_day = single_day.drop(['headline', 'compound'], axis=1)  
# Change the column names to 'negative', 'positive', and 'neutral'
plot_day.columns = ['negative', 'positive', 'neutral']
# Plot a stacked bar chart
# ... YOUR CODE FOR TASK 9 :-) ...
plot_day.plot.bar(kind='stack')

