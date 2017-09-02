try:
    from config import conf
    from twitter import tweet_filter
    import tweepy, json
    from tweepy import Stream
    from tweepy.streaming import StreamListener
    from tweepy import OAuthHandler
except ImportError as e:
    print("Import Error in streaming.py:", e)
    quit()

auth = OAuthHandler(conf['ckey'], conf['csecret'])
auth.set_access_token(conf['atoken'], conf['asecret'])
api = tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

class Listener(StreamListener):
    # Override Tweepy's Listener class, on_data and on_error
    def __init__(self, lim, coll, count, message):
        super().__init__()
        self.count = count
        self.lim = lim
        self.coll = coll
        self.message = message

    def on_data(self, data):
        # Manage retrieved json doc
        if self.lim is not None and self.count >= self.lim:
            #print("\n" + str(self.count) + " tweets successfully inserted!")
            raise KeyboardInterrupt  # easy way to return to menus

        json_data = json.loads(data)
        if tweet_filter.social_filter(json_data): # Filter out RT's, Quotes, Replies
            if tweet_filter.duplicate_find(self.coll,json_data):  # Filter out duplicates
                self.count += 1
                self.coll.insert_one(json_data)
            if self.lim is not None: # Progress bar vs counter (unlimited tweets)
                print("\rTweets:", self.count,
                      "[{0:50s}] {1:.1f}% ".format('#' * int((self.count / int(self.lim)) * 50),
                                                   (self.count / int(self.lim)) * 100) + self.message, end='',flush=True)
            else:
                print("\rTweets:", self.count + self.message, end='',flush=True)
            return True

    def on_error(self, status):
        # Handle error codes
        print("Error code:", status, end=". ")
        if status == 420:
            print("Rate limit reached. Please try again later.")
        if status == 406:
            print("Invalid tweet search request.")
        if status == 401:
            print("Authentication failed. Check your keys and verify your system clock is accurate.")
        print("Streaming stopped.")
        raise KeyboardInterrupt


def stream(Setup):
    listener = None
    count = 0
    msg = ''
    while True:  # start streaming
        try:
            listener = Listener(Setup.lim, Setup.tweet_coll, count, msg)
            twitter_stream = Stream(auth, listener)
            twitter_stream.filter(track=Setup.term, languages=Setup.lang, follow=Setup.users)
        except KeyboardInterrupt:
            return
        except Exception as e:
            # print(" Error: ",e,", Attempting to continue...",end='')
            msg = ", Error at tweet " + str(listener.count) + ":" + str(e)
            if Setup.lim is not None:
                Setup.lim -= listener.count  # subtracts downloaded tweets from the limit for next round on error
            else:
                count = listener.count
            continue
