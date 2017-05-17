import config, tweepy
from tweepy import api
from tweepy import OAuthHandler
auth = OAuthHandler(config.ckey, config.csecret)
auth.set_access_token(config.atoken, config.asecret)
api = tweepy.API(auth)

def scrape():
    #http://stackoverflow.com/a/23996991
    max_tweets = 1000
    searched_tweets = []
    last_id = -1
    while len(searched_tweets) < max_tweets:
        count = max_tweets - len(searched_tweets)
        try:
            new_tweets = api.search(q=['a','b','c'], count=count, max_id=str(last_id - 1))

            if not new_tweets:
                break
            searched_tweets.extend(new_tweets)
            last_id = new_tweets[-1].id
            for i, k in enumerate(searched_tweets):
                print(i, k)
        except tweepy.TweepError as e:
            # depending on TweepError.code, one may want to retry or wait
            # to keep things simple, we will give up on an error
            break
scrape()

#QUERY USES https://dev.twitter.com/rest/public/search