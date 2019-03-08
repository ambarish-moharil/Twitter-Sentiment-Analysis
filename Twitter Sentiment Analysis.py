
# coding: utf-8

# # Sentiment Analysis Of Tweets

# In[13]:


# conda install twython
from twython import Twython


# In[14]:


# https://apps.twitter.com/
consumer_key = 'oFNYu2QOp1UbUArIei9jiRQCT'
consumer_secret = 'NDjBgUPnoCXBCfnQD2CdUAq9VnIB85SMlPB8jledp47pyMbOAw'
access_token = '841034064-MVx5Gq9S5HlSzkUYlSmZRO8IGH3vuAsb0Y7VTAK0'
access_token_secret = '9QBefJ6lpcPaumJt8v2XV5RIPqvDiib8oRd3d3xueBnND'


# In[15]:


twitter = Twython(consumer_key, consumer_secret,
                         access_token, access_token_secret)


# In[16]:


result_dict = twitter.search(q='FIFA', lang = 'en', count=2,result_type='popular')
print(result_dict)


# In[17]:


list_tweets = result_dict['statuses']
for tweet in list_tweets:
    print (tweet['text'])
    print('#############################################')


# # Twitter to MongoDB using Python

# In[4]:


# from twython import Twython
# import pymongo


# In[28]:


result_dict = twitter.search(q='FIFA', lang = 'en', count=5,result_type='popular')
list_tweets = result_dict['statuses']
for tweet in list_tweets:
    print (tweet['text'])
    print('#############################################')


# In[29]:


connection = pymongo.MongoClient()

mydb=connection.twitter
db_tweets = mydb.tweets


# In[30]:


db_tweets.insert_many(list_tweets)


# In[31]:


# Select from collection
records_all = db_tweets.find()

for record in records_all:
    print (record['text'])
    print(record['entities'])
    print(record['created_at'])
    print('###########################################')


# # Sentiment Analysis

# In[33]:


import re
# conda install -c conda-forge textblob
from textblob import TextBlob


# In[35]:


def clean_tweet(tweet):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        return (' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split()))


# In[39]:


def get_tweet_sentiment(tweet):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        # create TextBlob object of passed tweet text
        analysis = TextBlob(clean_tweet(tweet))
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return ('positive')
        elif analysis.sentiment.polarity == 0:
            return ('neutral')
        else:
            return ('negative')


# In[42]:


# Select from collection
records_all = db_tweets.find()
sentimets_total = {'neutral': 0 , 'positive' : 0 , 'negative':0}
for record in records_all:
    tweet_raw = record['text']
    sentiment = get_tweet_sentiment(tweet_raw)
    print (sentiment,'===>',record['text'])
    sentimets_total[sentiment] = sentimets_total[sentiment] + 1
    print('###########################################')
print(sentimets_total)


# In[45]:


from matplotlib import pyplot as plt
slices = [sentimets_total['neutral'],sentimets_total['positive'],sentimets_total['negative']]
activities = ['Neutral','Positive','Negative']
cols = ['c','m','r',]

plt.pie(slices,
        labels=activities,
        colors=cols,
        shadow= True,
        autopct='%1.1f%%')

plt.title('Sentiment Analysis of Tweets')
plt.legend()
plt.show()

