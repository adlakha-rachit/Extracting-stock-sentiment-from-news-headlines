import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import webbrowser
import urllib.parse
from urllib.parse import urlparse
import time
from openpyxl import load_workbook

import datetime as dt
from Google import Create_Service

from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA

market_time = 8
google_terms = ['Google','here','All','Images','Maps','Videos','Shopping','Books','Search Tools',
                'Blogs','Past hour','Past 24 hours','Past week','Past month','Past year','Archives',
                'Sorted by date','Next >','Sign in','Settings','Privacy','Terms','Search tools',
                'Search for English results only','Preferences','Recent','Skip to main content',
                'Accessibility help','Accessibility feedback','Search activity','Report inappropriate predictions',
                'More','Flights','Finance','Search settings','Languages','Turn on SafeSearch','Search activity',
                ' ','Your data in Search','Search help','Tools','View all','Create alert','Next','Send feedback','Help','Access Denied',None]
with open('dict.txt') as f:
    content = f.readlines()
content = [x.strip() for x in content]

words = {}

for x in content:
    x = x.split('>>>')
    x[0] = x[0].strip()
    x[1] = x[1].strip()
    words[x[0]] = float(x[1])
while market_time < 17 :
    try:
        CLIENT_SECRET_FILE = 'client_secret.json'
        API_SERVICE_NAME = 'sheets'
        API_VERSION = 'v4'
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        gsheetId = '1yJcUfSGcoB1ruqnyf2GnysKhqOeZ_gL7bel-6cftm7M'

        service = Create_Service(CLIENT_SECRET_FILE, API_SERVICE_NAME, API_VERSION, SCOPES)

        url = 'https://www.google.com/search?biw=698&bih=680&tbs=qdr%3Ah&tbm=nws&sxsrf=ALeKk01fh35u8QRkwEInf3Ph8s3wZLaGlw%3A1587103535167&ei=L0eZXsfwCce9rQHblq4g&q=nifty+live&oq=nifty+live&gs_l=psy-ab.3..0l7.4700.6332.0.6507.5.3.0.2.2.0.292.809.2-3.3.0....0...1c.1.64.psy-ab..0.5.827....0.3gVOGbHYeM0'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        html = requests.get(url,headers = headers)
        soup = BeautifulSoup(html.text,'lxml')
        news = soup.find_all('a')
        news_headlines = pd.DataFrame(columns=['Time','News','Compound','Positive','Neutral','Negative'])

        word = 'google'
        b = [i.get('href') for i in news if i.get('href')!=None ]
        for k in news:
            if k.get_text() in google_terms and k.get('href')!=None:
                b.remove(k.get('href'))
        try:
            b.remove('#')
            b.remove('https://www.google.co.in/intl/en/about/products?tab=nh')
        except:
            continue
        headlines = []

        for i in b :
            if word in str(i) or str(i).startswith('/search'):
                b.remove(i)


        if len(b)> 0:
            b = list(dict.fromkeys(b))
            
            
            for i in b:
                try:
                    url = str(i)
                    html = requests.get(url)
                    soup = BeautifulSoup(html.text,'lxml')
                    ti = soup.find('h1')
                    try:
                        if ti.get_text() != None and ti != None:
                            headlines.append(ti.get_text())
                    except:
                            continue
                except :
                    continue
                

            for i in headlines:
                i = i.strip()
            
            
                
            for i in headlines:
                sia = SIA()
                sia.lexicon.update(words)
                pol_score = sia.polarity_scores(i)
                news_headlines = news_headlines.append({'Time':(f'{market_time}' + ':15'),'News':i,'Compound':pol_score['compound'],'Positive':pol_score['pos'],'Neutral':pol_score['neu'],'Negative':pol_score['neg']},ignore_index=True)

            news_headlines['Date'] = dt.date.today()
            
            news_headlines.set_index('Date',inplace= True)
            news_headlines.to_csv('news.csv')
            
            market_time = market_time +1 
            
            def Export_Data_To_Sheets():
                t = dt.datetime.now().hour
                t = t - 8
                df = pd.read_csv('news.csv')

                response_date = service.spreadsheets().values().append(
                    spreadsheetId=gsheetId,
                    valueInputOption='RAW',
                    range=f'Sheet{t}!A1',
                    body=dict(
                        majorDimension='ROWS',
                        values=df.T.reset_index().T.values.tolist())
                ).execute()

            Export_Data_To_Sheets()
            
            time.sleep(3600)
            
        else :
            market_time = market_time + 1
            time.sleep(3600)
             
    except:
        print('exception')
        market_time = market_time +1
        time.sleep(3600)
        
        
