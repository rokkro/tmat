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
    print("Retrieving tweets...")
    while len(searched_tweets) < Setup.lim:
        count = Setup.lim - len(searched_tweets)
        try:
            new_tweets = api.search(q=Setup.term,result_type=Setup.result_type,until=Setup.until, count=count, max_id=str(last_id - 1))
            if not new_tweets:
                break
            searched_tweets.extend(new_tweets)
            last_id = new_tweets[-1].id
            for iter, json_data in enumerate(searched_tweets):
                if tweet_filter.json_filter(json_data._json):
                    if not tweet_filter.duplicate_find(Setup.tweet_coll, json_data._json,
                                                       Setup.sim):  # if no duplicates found, add tweet to db
                        Setup.tweet_coll.insert_one(json_data._json)
            print(Color.END,end='')
            print("\rTweets:", len(searched_tweets),
                  "[{0:50s}] {1:.1f}% ".format('#' * int((len(searched_tweets) / int(Setup.lim)) * 50),
                                               (len(searched_tweets) / int(Setup.lim)) * 100), end="", flush=True)

        except Exception as e:
            print(e)
            break
