try:
    from twitter import tweet_filter
    import config, tweepy
    from tweepy import api
    from tweepy import OAuthHandler
except ImportError as e:
    print("Import Error in historic.py:", e)

auth = OAuthHandler(config.ckey, config.csecret)
auth.set_access_token(config.atoken, config.asecret)
api = tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

def scrape(Setup):
    """
    References used: http://stackoverflow.com/a/23996991
    https://dev.twitter.com/rest/reference/get/search/tweets
    https://dev.twitter.com/rest/public/search
    https://dev.twitter.com/rest/public/timelines
    """
    searched_tweets = []
    last_id = -1
    successful = 0
    while successful < Setup.lim: # While haven't hit specified limit.
        count = Setup.lim - successful
        try:
            new_tweets = api.search(q=Setup.term,result_type=Setup.result_type,
                                    until=Setup.before, count=count, max_id=str(last_id - 1))
            if not new_tweets: # Stop when run out of tweets.
                break
            searched_tweets.extend(new_tweets) # The 'new' tweets
            last_id = new_tweets[-1].id  # Used to track which tweets to get next.

            for iter, data in enumerate(searched_tweets):
                if tweet_filter.social_filter(data._json): # Filter out replies, quotes, RT's
                    if tweet_filter.duplicate_find(Setup.tweet_coll, data._json):  # Filter out duplicates
                        if Setup.after is None or tweet_filter.date_filter(data._json,Setup.after): # Filter date
                            Setup.tweet_coll.insert_one(data._json) # Insert into DB
                            successful+=1

            searched_tweets[:] = [] # Empty tweets for next batch.
            print("\rTweets:", successful, # Counter
                  "[{0:50s}] {1:.1f}% ".format('#' * int((successful / int(Setup.lim)) * 50),
                                               (successful / int(Setup.lim)) * 100), end='',flush=True)
        except tweepy.TweepError as e:
            print("Error:",e.args[0])
            return
        except Exception as e:
            print("Error:",e)
