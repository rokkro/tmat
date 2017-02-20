import tweepy, json, string, configparser
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from http.client import IncompleteRead
from pymongo import MongoClient

try:
    config = configparser.ConfigParser()
    config.read('config.ini')
    ckey = config['TWITTER']['consumer-key']
    csecret = config['TWITTER']['consumer-secret']
    atoken = config['TWITTER']['access-token']
    asecret = config['TWITTER']['access-secret']
except KeyError:
    print("Make sure you put your keys in config.ini.")
    quit()

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
api = tweepy.API(auth)
client = MongoClient() #mogno
db = client.test_database #db
tweets = db.tweets #collection

class Listener(StreamListener):
    def __init__(self,lim): #constructor
        self.count = 0
        self.lim = lim

    def on_data(self, data):
        if self.count == self.lim:
            quit()
        dataj = json.loads(data)
        if self.json_filter(dataj):
            try:
                if not self.duplicate_find(dataj): #if no duplicates found, add tweet to db
                    self.count += 1
                    tweets.insert_one(dataj)
                if self.lim != None:
                    print("\rTweets:", self.count, "[{0:50s}] {1:.1f}% ".format('#' * int((self.count / int(self.lim)) * 50),(self.count / int(self.lim)) * 100), end="", flush=True)
                else:
                    print("\rTweets:",self.count,end="",flush=True)
                return True

            except Exception as e:
                print("\nError in on_data: ",e,"\nStreaming stopped.")
                quit()

    def duplicate_find(self, dataj):
        try:
            cursor = db.tweets.find({'user.screen_name': dataj['user']['screen_name']})
            for c in cursor:  # searching for exact same tweets from same user, removing spaces and punct. Spaces take a lot of effort to remove
                cursorText = " ".join(c['text'].translate(c['text'].maketrans('','',string.punctuation)).replace(" ","").split())
                datajText = " ".join(dataj['text'].translate(dataj['text'].maketrans('','',string.punctuation)).replace(" ","").split())
                if cursorText == datajText:
                    print(" STEXT: " + c['text'] + " DTEXT: " + datajText)
                    print("\nDuplicate tweet from " + "@" + dataj['user']['screen_name'] + " ignored.")
                    return True
            return False #if no duplicates found
        except Exception as e:
            print("Error in duplicate_find. This might be an issue with your MongoDB service - see:",e)
            #eturn True
            quit()

    def json_filter(self,dataj): #not a superclass method. Removes certain tweets
        try:
            if "created_at" not in dataj or "retweeted_status" in dataj or\
                            "quoted_status" in dataj or dataj["in_reply_to_user_id"] != None:
                return False
            else:
                return True #does NOT affect tweet streaming. Whether or not tweet saved
        except Exception as e:
            print("Error in json_filter: ",e)
            quit()

    def on_error(self, status):
        print("Error code:",status,end=". ")
        if status == 406:
            print("Invalid tweet search request.")
        if status == 401:
            print("Authentication failed. Check your keys or verify your system clock is accurate.")
        if status == 420:
            print("Rate limit reached. Wait a bit before streaming again.")
        print("Streaming stopped.")
        quit()

def limit():
    while True:
        lim = input("Enter number of tweets to retrieve (integer only): ")
        try:
            lim=int(lim)
            if lim<0:
                continue
            break
        except ValueError:
            print("Invalid Input.")
            continue
    return lim

def stream(lim=None):
    while True:
        search = " ".join(input("Enter a search term or hashtag:").split())
        if search == '':
            print("Invalid Input.")
            continue
        break
    while True:
        try:
            print("Searching for tweets...")
            l = Listener(lim)
            twitter_stream = Stream(auth,l)
            twitter_stream.filter(track=[search], async=False)
        except IncompleteRead: #exception occurs when tweets fall behind
            print("Error: Incomplete Read occurred. Skipping to newer tweets.")
            continue

if __name__ == '__main__':
    try:
        stream(limit())
    except KeyboardInterrupt:
        pass