import tweepy
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

    def on_data(self, data):
        if str(self.count) == self.lim:
            return False #stop streaming if hits tweet limit
        try:
            with open('live.json', 'a') as f: #currently appends to file, may change later
                f.write(data + "\n")
                self.count += 1
                print("Tweets retrieved: " + str(self.count))
                return True
        except Exception as e:
            print("Possible .json write error. Error: " + str(e))
            return False #stops streaming on write error

    def on_error(self, status):
        print("Error code:",status)
        if status == 406:
            print("Invalid tweet search request.")
        if status == 401:
            print("Authentication failed. Check your keys or verify your system clock is accurate.")
        return False #quits streaming if error


def stream():
    search = input("Enter a search term or hashtag:")
    lim = input("Enter number of tweets to retrieve (integers only). Leave blank if unlimited: ")
    l = Listener(lim)
    twitter_stream = Stream(auth,l)
    twitter_stream.filter(track=[search], async=True)

if __name__ == '__main__':
    stream()
