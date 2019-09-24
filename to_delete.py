import nltk
import csv
import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import time
import pprint

import warnings
warnings.filterwarnings('ignore')

from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()

date_sentiments = {}

for i in range(1,5):
    page = urlopen('https://www.businesstimes.com.sg/search/facebook?page='+str(i)).read()
    soup = BeautifulSoup(page, features="html.parser")
    posts = soup.findAll("div", {"class": "media-body"})
    for post in posts:
        time.sleep(1)
        url = post.a['href']
        date = post.time.text
        print(date, url)
        try:
            link_page = urlopen(url).read()
        except:
            pass
        link_soup = BeautifulSoup(link_page)
        sentences = link_soup.findAll("p")
        passage = ""
        for sentence in sentences:
            passage += sentence.text
        #print("The Entire Passage is \n",  passage)
        sentiment = sia.polarity_scores(passage)['compound']
        date_sentiments.setdefault(date, []).append(sentiment)
        
date_sentiment = {}

for k,v in date_sentiments.items():
    date_sentiment[datetime.strptime(k, '%d %b %Y').date() + timedelta(days=1)] = round(sum(v)/float(len(v)),3)

earliest_date = min(date_sentiment.keys())

print(date_sentiment)

#############################################################################################################################################

'''
REFERENCE SECTION

IN THE FOLLOWING LINK JUST USE THE NAME OF THE STOCK/COMPANY YOU WANT TO SCRAP NEWS ABOUT.
TO GET THE ARTICLES FROM MORE PAGES JUST INCREASE UPPER BOUND IN THE RANGE IN LINE 16.
THE FOLLOWING SCRIPT HAS TO BE RUN IN THE COMMAND LINE AND IT WOULD SCRAPE ALL THE ARTICLES FROM THE LINK GIVEN.
THE NEWEST ARTICLES ALSO AND THE OLDEST ARTICLE ALSO.
'''




