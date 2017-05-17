from twitter import tweet_filter
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
    while len(searched_tweets) < Setup.lim:
        count = Setup.lim - len(searched_tweets)
        try:
            new_tweets = api.search(q=Setup.term,result_type=Setup.result_type,until=Setup.until, count=count, max_id=str(last_id - 1))
            if not new_tweets:
                break
            searched_tweets.extend(new_tweets)
            last_id = new_tweets[-1].id
            for iter, json_data in enumerate(searched_tweets):
                if tweet_filter.json_filter(json_data):
                    if not tweet_filter.duplicate_find(Setup.tweet_coll, json_data,
                                                       Setup.sim):  # if no duplicates found, add tweet to db
                        Setup.tweet_coll.insert_one(json_data)

                print(iter, json_data)
        except tweepy.TweepError as e:
            print(e)
            break

#USES https://dev.twitter.com/rest/public/search