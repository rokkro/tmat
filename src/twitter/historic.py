from twitter import tweet_filter
from display import Color
import config, tweepy
from tweepy import api
from tweepy import OAuthHandler

auth = OAuthHandler(config.ckey, config.csecret)
auth.set_access_token(config.atoken, config.asecret)
api = tweepy.API(auth)

def scrape(Setup):
    #http://stackoverflow.com/a/23996991
    searched_tweets = []
    last_id = -1
    successful = 0
    print("Retrieving tweets...")
    print(Color.END,end='')
    while successful < Setup.lim:
        count = Setup.lim - successful  #len(searched_tweets)
        try:
            new_tweets = api.search(q=Setup.term,result_type=Setup.result_type,until=Setup.until, count=count, max_id=str(last_id - 1))
            if not new_tweets:
                break
            searched_tweets.extend(new_tweets)
            last_id = new_tweets[-1].id
            for iter, data in enumerate(searched_tweets):
                if tweet_filter.json_filter(data._json):
                    if not tweet_filter.duplicate_find(Setup.tweet_coll, data._json,
                                                       Setup.sim):  # if no duplicates found, add tweet to db
                        Setup.tweet_coll.insert_one(data._json)
                        successful+=1
            searched_tweets[:] = []
            print("\rTweets:", successful,
                  "[{0:50s}] {1:.1f}% ".format('#' * int((successful / int(Setup.lim)) * 50),
                                               (successful / int(Setup.lim)) * 100), end="", flush=True)
        except Exception as e:
            print("Error:",e)
            continue
