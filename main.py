import tweepy, json
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener


ckey = ""
csecret = ""
atoken = ""
asecret = ""

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
api = tweepy.API(auth)

class Listener(StreamListener):
    def __init__(self,lim): #constructor
        self.count = 0
        self.lim = lim
        self.kill = False #set to true to stop streaming

    def on_data(self, data):
        if self.count == self.lim or self.kill:
            return False #stop streaming if hit limit or is ordered to from outside
        if self.json_filter(data):
            try:
                with open('live.json', 'a') as f: #currently appends to file, may change later
                    f.write(data + "\n")
                    self.count += 1
                    if self.lim != None:
                        print("\rProgress: [{0:50s}] {1:.1f}% , Tweets: ".format('#' * int((self.count / int(self.lim)) * 50),(self.count / int(self.lim)) * 100),self.count, end="", flush=True)
                    else:
                        print("\rTweets:",self.count,end="",flush=True)
                    return True
            except Exception as e:
                print("Error in on_data: " + str(e) + "\nStreaming stopped.")
                return False #stops streaming on write error

    def kill(self): #needs this to work I guess
        self.kill=True

    def json_filter(self,data): #not a superclass method. Removes certain tweets
        try:
            jdata = json.loads(data)
            if "created_at" not in jdata or "retweeted_status" in jdata or\
                            "quoted_status" in jdata or jdata["in_reply_to_user_id"] != None:
                return False
            else:
                return True #does NOT affect tweet streaming. Whether or not tweet saved
        except Exception as e:
            print("Error in json_filter: " + str(e))
            return False

    def on_error(self, status):
        print("Error code:",status,end=". ")
        if status == 406:
            print("Invalid tweet search request.")
        if status == 401:
            print("Authentication failed. Check your keys or verify your system clock is accurate.")
        print("Streaming stopped.")
        return False #quits streaming if error


def stream():
    search = input("Enter a search term or hashtag:")
    lim = input("Enter number of tweets to retrieve (integer only). Leave blank if unlimited: ")
    try:
        lim = int(lim)
        if lim < 0:
            raise ValueError
    except ValueError:
        print("No tweet limit set.")
        lim = None
    l = Listener(lim)
    twitter_stream = Stream(auth,l)
    twitter_stream.filter(track=[search], async=False)

if __name__ == '__main__':
    try:
        stream()
    except KeyboardInterrupt:
        pass
