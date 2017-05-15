try:
    import config, requests
    import tweepy, json,string
    from display import Color
    from tweepy import Stream
    from tweepy.streaming import StreamListener
    from tweepy import OAuthHandler
    from http.client import IncompleteRead
    from difflib import SequenceMatcher
except ImportError as e:
    print("Error:", e)
    quit()

auth = OAuthHandler(config.ckey, config.csecret)
auth.set_access_token(config.atoken, config.asecret)
api = tweepy.API(auth)

class Listener(StreamListener):
    def __init__(self, lim, coll, sim):
        super().__init__()
        self.count = 0
        self.lim = lim
        self.coll = coll
        self.sim = sim

    def on_data(self, data):
        if self.lim is not None and self.count >= self.lim:
            print(Color.YELLOW,end="")
            print("\n" + str(self.count) + " tweets successfully inserted!")
            raise KeyboardInterrupt  # easy way to return to menus

        json_data = json.loads(data)
        if self.json_filter(json_data):
            if not self.duplicate_find(json_data):  # if no duplicates found, add tweet to db
                self.count += 1
                self.coll.insert_one(json_data)
            print(Color.END,end="")
            if self.lim is not None:
                print("\rTweets:", self.count,
                      "[{0:50s}] {1:.1f}% ".format('#' * int((self.count / int(self.lim)) * 50),
                                                   (self.count / int(self.lim)) * 100), end="", flush=True)
            else:
                print("\rTweets:", self.count, end="", flush=True)
            return True

    def duplicate_find(self, json_data):
        cursor = self.coll.find({'user.screen_name': json_data['user']['screen_name']})
        for c in cursor:  # searching for exact same tweets from same user, removing spaces and punct.
            coll_tweet = c['text'].translate(c['text'].maketrans('', '', string.punctuation)).replace(" ", "")
            json_tweet = json_data['text'].translate(json_data['text'].maketrans('', '', string.punctuation)).replace(
                " ", "")

            if coll_tweet == json_tweet:
                if config.verbose:
                    print(" FIRST: " + c['text'] + " SECOND: " + json_data['text'])
                    print("\nDuplicate tweet from " + "@" + json_data['user']['screen_name'] + " ignored.")
                cursor.close()
                return True
            elif SequenceMatcher(None, coll_tweet, json_tweet).ratio() > self.sim:
                if config.verbose:
                    print("\n" + str(SequenceMatcher(None, coll_tweet, json_tweet).ratio() * 100) + "% similar existing"
                                                                                                    " tweet from " + "@" +
                          json_data['user']['screen_name'] + " ignored.")
                    print(" FIRST: " + c['text'] + " SECOND: " + json_data['text'])
                cursor.close()
                return True

        cursor.close()
        return False  # if no duplicates found

    def json_filter(self, json_data):  # removes certain tweets
        if "created_at" not in json_data or "retweeted_status" in json_data or \
                        "quoted_status" in json_data or json_data["in_reply_to_user_id"] != None:
            return False
        return True  # does NOT affect tweet streaming. Whether or not tweet saved

    def on_error(self, status):
        print("Error code:", status, end=". ")
        if status == 406:
            print("Invalid tweet search request.")
        if status == 401:
            print("Authentication failed. Check your keys and verify your system clock is accurate.")
        if status == 420:
            print("Rate limit reached. Wait a bit before streaming again.")
        print("Streaming stopped.")
        quit()


def stream(Setup):
    listener = None
    while True:  # start streaming
        try:
            listener = Listener(Setup.lim, Setup.tweet_coll, Setup.sim)
            print("Waiting for new tweets...")
            twitter_stream = Stream(auth, listener)
            twitter_stream.filter(track=Setup.term, languages=Setup.lang, follow=Setup.users)  # location search is not a filter
        except KeyboardInterrupt:
            return
        except IncompleteRead:
            print("Incomplete Read - Skipping to newer tweets.\n")
        except requests.exceptions.ConnectionError:
            print("Connection Failed - Check your internet.")
            return
        except Exception as e:
            if Setup.lim is not None:
                Setup.lim -= listener.count  # subtracts downloaded tweets from the limit for next round
            #print("Error: ",e,"\nAttempting to continue...\n")
            continue
