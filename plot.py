import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt


scored_news = pd.read_csv('news.csv')


single_day = scored_news.set_index(['Date'])

#Date for which sentiment is plotted
single_day = single_day.loc['2020-12-22']
single_day['Time'] = pd.to_datetime(single_day['Time'])
single_day['Time'] = single_day.time.dt.time 

single_day = single_day.set_index('Time')

single_day = single_day.sort_index(ascending = True)


TITLE = "Positive, negative and neutral sentiment for Nifty on Date"
COLORS = ["red", "orange", "green"]
plot_day = single_day.drop(['News', 'compound'], axis=1)
plot_day.columns = ['negative', 'positive', 'neutral']
plot_day.plot.bar(stacked = True, 
                  figsize=(10, 6), 
                  title = TITLE, 
                  color = COLORS).legend(bbox_to_anchor=(1.2, 0.5))