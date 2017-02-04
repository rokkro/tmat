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
    def __init__(self,count,lim):
        self.count = count
        self.lim = lim

    def on_data(self, data):
        if str(self.count) == self.lim:
            return False
        try:
            with open('live.json', 'a') as f:
                f.write(data)
                self.count += 1
                print("tweets retrieved " + str(self.count) + "\r")
                return True
        except BaseException as e:
            print("on_data: " + str(e))
        return True

    def on_error(self, status):
        print("Error code:",status)
        if status == 406:
            print("Invalid tweet search request.")
        if status == 401:
            print("Authentication failed. Check your keys or verify your system clock is accurate.")
        return False #quits streaming if error
def stream():
    count = 0
    search = input("Enter a search term or hashtag:")
    lim =input("Enter number of tweets to retrieve (integers only). Leave blank if unlimited: ")
    twitter_stream = Stream(auth, Listener(count,lim))
    twitter_stream.filter(track=[search], async=True)

if __name__ == '__main__': #execute this module if
     stream()
