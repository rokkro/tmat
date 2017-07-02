try:
    import config
    from twitter import tweet_filter
    import tweepy, json
    from tweepy import Stream
    from tweepy.streaming import StreamListener
    from tweepy import OAuthHandler
except ImportError as e:
    print("Error:", e)
    quit()

auth = OAuthHandler(config.ckey, config.csecret)
auth.set_access_token(config.atoken, config.asecret)
api = tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

class Listener(StreamListener):
    def __init__(self, lim, coll):
        super().__init__()
        self.count = 0
        self.lim = lim
        self.coll = coll

    def on_data(self, data):
        if self.lim is not None and self.count >= self.lim:
            #print("\n" + str(self.count) + " tweets successfully inserted!")
            raise KeyboardInterrupt  # easy way to return to menus

        json_data = json.loads(data)
        if tweet_filter.social_filter(json_data):
            if tweet_filter.duplicate_find(self.coll,json_data):  # if no duplicates found, add tweet to db
                self.count += 1
                self.coll.insert_one(json_data)
            if self.lim is not None:
                print("\rTweets:", self.count,
                      "[{0:50s}] {1:.1f}% ".format('#' * int((self.count / int(self.lim)) * 50),
                                                   (self.count / int(self.lim)) * 100), end='',flush=True)
            else:
                print("\rTweets:", self.count, end='',flush=True)
            return True

    def on_error(self, status):
        print("Error code:", status, end=". ")
        if status == 406:
            print("Invalid tweet search request.")
        if status == 401:
            print("Authentication failed. Check your keys and verify your system clock is accurate.")
        print("Streaming stopped.")
        raise KeyboardInterrupt


def stream(Setup):
    listener = None
    while True:  # start streaming
        try:
            listener = Listener(Setup.lim, Setup.tweet_coll)
            twitter_stream = Stream(auth, listener)
            twitter_stream.filter(track=Setup.term, languages=Setup.lang, follow=Setup.users)  # location search is not a filter
        except KeyboardInterrupt:
            return
        except Exception as e:
            print("Error: ",e,"\nAttempting to continue...\n")
            if Setup.lim is not None:
                Setup.lim -= listener.count  # subtracts downloaded tweets from the limit for next round
            continue
