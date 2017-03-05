try:
    import tweepy, json, string, configparser, datetime
    from tweepy import Stream
    from tweepy import OAuthHandler
    from tweepy.streaming import StreamListener
    from pymongo import MongoClient
    from pymongo.errors import ConnectionFailure
    from http.client import IncompleteRead

    config = configparser.ConfigParser()
    config.read('config.ini')
    ckey = config['TWITTER']['consumer-key']
    csecret = config['TWITTER']['consumer-secret']
    atoken = config['TWITTER']['access-token']
    asecret = config['TWITTER']['access-secret']
except KeyError as e:
    print("Error: verify you put your keys in config.ini:", e)
    quit()
except ImportError as e:
    print("Error: module missing/not installed:", e)
    quit()

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
api = tweepy.API(auth)
client = None

class Listener(StreamListener):
    def __init__(self, lim, tweetcoll):  # constructor
        self.count = 0
        self.lim = lim
        self.tweetcoll = tweetcoll

    def on_data(self, data):
        if self.count == self.lim:
            quit()
        dataj = json.loads(data)
        if self.json_filter(dataj):
            try:
                if not self.duplicate_find(dataj):  # if no duplicates found, add tweet to db
                    self.count += 1
                    self.tweetcoll.insert_one(dataj)
                if self.lim != None:
                    print("\rTweets:", self.count,
                          "[{0:50s}] {1:.1f}% ".format('#' * int((self.count / int(self.lim)) * 50),
                                                       (self.count / int(self.lim)) * 100), end="", flush=True)
                else:
                    print("\rTweets:", self.count, end="", flush=True)
                return True
            except Exception as e:
                print("\nError in on_data: ", e, "\nStreaming stopped.")
                quit()
            except ConnectionFailure as e:
                print("Error: MongoDB connection refused, verify MongoDB is running:", e)
                quit()

    def duplicate_find(self, dataj):
        cursor = self.tweetcoll.find({'user.screen_name': dataj['user']['screen_name']})
        for c in cursor:  # searching for exact same tweets from same user, removing spaces and punct.
            cursorText = c['text'].translate(c['text'].maketrans('', '', string.punctuation)).replace(" ", "")
            datajText = dataj['text'].translate(dataj['text'].maketrans('', '', string.punctuation)).replace(" ", "")
            if cursorText == datajText:
                # print(" STEXT: " + c['text'] + " DTEXT: " + datajText)
                print("\nDuplicate tweet from " + "@" + dataj['user']['screen_name'] + " ignored.")
                return True
        return False  # if no duplicates found

    def json_filter(self, dataj):  # not a superclass method. Removes certain tweets
        try:
            if "created_at" not in dataj or "retweeted_status" in dataj or \
                            "quoted_status" in dataj or dataj["in_reply_to_user_id"] != None:
                return False
            else:
                return True  # does NOT affect tweet streaming. Whether or not tweet saved
        except Exception as e:
            print("Error in json_filter: ", e)
            quit()

    def on_error(self, status):
        print("Error code:", status, end=". ")
        if status == 406:
            print("Invalid tweet search request.")
        if status == 401:
            print("Authentication failed. Check your keys or verify your system clock is accurate.")
        if status == 420:
            print("Rate limit reached. Wait a bit before streaming again.")
        print("Streaming stopped.")
        quit()


class Setup():
    def __init__(self):
        self.temp = False
        self.img = False
        self.db_name = 'twitter'
        self.connected = False
        self.dt = str(datetime.datetime.now())

    def mongo_handler(self):
        global client
        if self.connected:
            print("Disconnected from MongoDB.")
            client.close()
            self.connected = False
        else:
            print("Attempting connection to MongoDB...")
            try:
                client = MongoClient()
                self.dbname_list = client.database_names()
                print("Connection Succeeded!")
                self.connected = True
            except ConnectionFailure as e:
                print("Error: MongoDB not connected:", e)
            except Exception as e:
                print("Error:", e)

    def get_collections(self):
        return client[self.db_name].collection_names()

    def limit(self):
        while True:
            self.lim = input("*Enter number of tweets to retrieve. Leave blank for unlimited: ")
            try:
                if self.lim == '': #if no input
                    self.lim = None #set limit to None/unlimited
                    break
                self.lim = int(self.lim) #typecast to int, filtering out invalid characters
                if self.lim < 0: #no negative nums
                    continue
            except ValueError:
                print("Invalid Input.")
                continue
            break
        return self.lim

    def search(self):
        self.term = [] #contains actual search terms
        tmp = [] #stores user input to filter out invalid responses
        while True:
            i = input("*Enter search term(s), separate multiple terms with '||' :").strip()
            if i == '': #no input
                print("You must enter at least one search term.")
                continue
            tmp = i.split('||') #split into list by ||
            for i in range(len(tmp)):
                tmp[i] = tmp[i].strip()  #remove outside spacing from all entries
                if tmp[i] == '': #if blank after spaces removed, dont append to search term list
                    continue
                self.term.append(tmp[i])
            if len(self.term) == 0: #if nothing appended to search term list, restart.
                continue
            self.coll_name = self.term[0] + " - " + self.dt #set initial collection name
            break
        return self.term


def stream(search, lim, coll_name, db_name, temp=False):  # search, limit, collection name
    db = client[db_name]  # db
    tweetcoll = db[coll_name]  # collection
    tweetcoll.insert_one({ #insert document marking collection as temp/not temp
        "temp" : temp
    })
    while True:
        try:
            listener = Listener(lim, tweetcoll)
            print("Waiting for new tweets...")
            twitter_stream = Stream(auth, listener)
            twitter_stream.filter(track=search)
        except KeyboardInterrupt:
            print("\n")
            break
        except IncompleteRead:
            print("Incomplete Read - Skipping to newer tweets.")
        except Exception as e:
            print("Error: ",e,"\nAttempting to continue...\n")
            continue

if __name__ == '__main__':
    try:
        s = Setup()
        s.mongo_handler()
        search = s.search()
        lim = s.limit()  # assigned to variables to make that print statement look nice
        print("Collection: " + s.coll_name + ", Database: " + s.db_name)
        if s.connected:
            stream(search, lim, s.coll_name, s.db_name, s.temp)  # remove limit() for unlimited if running this
        else:
            print("MongoDB not connected/running. Cannot stream.")
    except BaseException as e:
        print("Error:",e)
    except KeyboardInterrupt:
        pass
