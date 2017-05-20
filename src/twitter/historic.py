try:
    from twitter import tweet_filter
    from display_menu import Color
    import config, tweepy, time
    from tweepy import api
    from tweepy import OAuthHandler
except ImportError as e:
    print("Error:", e)
    quit()

auth = OAuthHandler(config.ckey, config.csecret)
auth.set_access_token(config.atoken, config.asecret)
api = tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

def scrape(Setup):
    #http://stackoverflow.com/a/23996991
    searched_tweets = []
    last_id = -1
    successful = 0
    print("Retrieving tweets...")
    while successful < Setup.lim:
        print(Color.END, end='')
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
        except tweepy.TweepError as e:
            print(Color.YELLOW,end='')
            error = e.args[0][0]['code']
            if error == 215:
                print("Authentication failed. Check your keys and verify your system clock is accurate.")
                return
            if error == 130 or error == 131:
                print("An error occurred on Twitter's end. Please try again...")
                return
            print("Error:",e)
            continue
