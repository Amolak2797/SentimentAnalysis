import re
import textblob
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
print("All imports ran successfully")

class TwitterClient(object):

    '''
    Generic Twitter Class for Sentiment Analysis
    '''

    def __init__(self):
        #keys and tokens for the Twitter Developer Account
        consumer_key='Fpusg9214p27fn0ZtDGEaVIBa'
        consumer_secret='jXxunmvAH8q42yPkAWd5DcCz8f0dNWRYQic8NBK18J87J3K0gg'
        print(consumer_key+"\n"+consumer_secret)
        access_token='1021966427530645504-0A2RK9F1WmxFgtkjLASTFZQnALfHbQ'
        access_token_secret='EZSQGm0r4EkqIJxAtzfmXK9O9ytWSNCbUu3DVntvcfkvi'
        print(access_token+"\n"+access_token_secret)
        try:
            #create OAuthHandler object
            self.auth=OAuthHandler(consumer_key,consumer_secret)
            
            #set access token and secret
            self.auth.set_access_token(access_token,access_token_secret)
            
            #create tweepy API object tofetch tweets
            self.api=tweepy.API(self.auth)
        except:
            print("Error: Authentication failed")

    def clean_tweet(self,tweet):
        '''
        Utility function to clean tweet text by removing links,special characters
        using simple regex statements.
        '''
        
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def get_tweet_sentiment(self,tweet):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        analysis=TextBlob(self.clean_tweet(tweet))
        if analysis.sentiment.polarity>0:
            return 'positive'
        elif analysis.sentiment.polarity==0:
            return 'neutral'
        else:
            return 'negative'
        
    def get_tweets(self,query,count=10):
        '''
        Main function to fetch twwets and parse them.
        '''
        #empty list to store parsed tweets

        print('Inside get tweets function')
        tweets=[]
        try:
            # call twitter api to fetch tweets
            fetched_tweets=self.api.search(q=query,count=count)

            #parsing tweets one by one
            for tweet in fetched_tweets:
                parsed_tweet={}
                parsed_tweet['text']=tweet.text
                #parsed_tweet['sentiment']=self.get_tweet_sentiment(tweet)
                print(tweet.text)

                #appending parsed tweet to tweets list
                if tweet.retweet_count>0:
                    #if tweet has retweets , ensure that it is appended only once
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                     tweets.append(parsed_tweet)
                #print(tweet.text)

            return tweets
        except tweepy.TweepError as e:
            print('Error : '+str(e))


def main():
    print('Main execution started')
    api=TwitterClient()
    print('Calling function get_tweets')
    tweets=api.get_tweets(query='Mahesh Babu',count=10)

    #picking positive tweets
    '''
    ptweets = [tweet for tweet in tweets if tweet['sentiment']=='positive']
    print('Positive tweets percentage : %f'%(100*len(ptweets)/len(tweets)))

    ntweets = [tweet for tweet in tweets if tweet['sentiment']=='negative']
    print('Negative tweets percentage : %f'%(100*len(ntweets)/len(tweets)))
    '''
    

main()
