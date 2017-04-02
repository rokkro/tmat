try:
    import mongo, config,requests
    import tweepy, json, string, datetime
    from tweepy import Stream
    from tweepy import OAuthHandler
    from tweepy.streaming import StreamListener
    from http.client import IncompleteRead
    from difflib import SequenceMatcher
except ImportError as e:
    print("Error: module missing/not installed:", e)
    quit()

auth = OAuthHandler(config.ckey, config.csecret)
auth.set_access_token(config.atoken, config.asecret)
api = tweepy.API(auth)

class Listener(StreamListener):
    def __init__(self, lim, coll, simil):
        self.count = 0
        self.lim = lim
        self.coll = coll
        self.simil = simil

    def on_data(self, data):
        if self.count == self.lim:
            raise KeyboardInterrupt #easy way to return to menus
        dataj = json.loads(data)
        if self.json_filter(dataj):
            if not self.duplicate_find(dataj):  # if no duplicates found, add tweet to db
                self.count += 1
                self.coll.insert_one(dataj)
            if self.lim != None:
                print("\rTweets:", self.count,
                      "[{0:50s}] {1:.1f}% ".format('#' * int((self.count / int(self.lim)) * 50),
                                                   (self.count / int(self.lim)) * 100), end="", flush=True)
            else:
                print("\rTweets:", self.count, end="", flush=True)
            return True

    def duplicate_find(self, dataj):
        cursor = self.coll.find({'user.screen_name': dataj['user']['screen_name']})
        for c in cursor:  # searching for exact same tweets from same user, removing spaces and punct.
            cursorText = c['text'].translate(c['text'].maketrans('', '', string.punctuation)).replace(" ", "")
            datajText = dataj['text'].translate(dataj['text'].maketrans('', '', string.punctuation)).replace(" ", "")
            if cursorText == datajText:
                #print(" FIRST: " + c['text'] + " SECOND: " + dataj['text'])
                #print("\nDuplicate tweet from " + "@" + dataj['user']['screen_name'] + " ignored.")
                return True
            elif SequenceMatcher(None,cursorText,datajText).ratio() > self.simil:
                #print("\n" + str(SequenceMatcher(None,cursorText,datajText).ratio() * 100) + "% similar existing"
                #     " tweet from " + "@" + dataj['user']['screen_name'] + " ignored.")
                #print(" FIRST: " + c['text'] + " SECOND: " + dataj['text'])
                return True
        return False  # if no duplicates found

    def json_filter(self, dataj):  #removes certain tweets
        if "created_at" not in dataj or "retweeted_status" in dataj or \
                        "quoted_status" in dataj or dataj["in_reply_to_user_id"] != None:
            return False
        else:
            return True  # does NOT affect tweet streaming. Whether or not tweet saved

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


class Setup(): #settings and setup for tweet scraping
    def __init__(self):
        self.temp = False
        self.img = False
        self.lim = None
        self.db_name = 'twitter'
        self.dt = str(datetime.datetime.now())
        self.sim = .55
        self.lang = ['en']
        self.coll_name = self.dt
        self.term = []
        self.users = []

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

    def search(self):
        tmp = [] #stores user input to filter out invalid responses
        i = input("*Enter search term(s), separate multiple queries with '||'.\n>>>").strip()
        if i == 'r':
            return
        self.term[:] = []
        if i == '':
            self.coll_name = self.dt
            return
        tmp = i.split('||') #split into list by ||
        for i in range(len(tmp)):
            tmp[i] = tmp[i].strip()  #remove outside spacing from all entries
            if tmp[i] == '': #if blank after spaces removed, dont append to search term list
                continue
            self.term.append(tmp[i])
        if len(self.term) == 0: #if nothing appended to search term list, return.
            return
        self.coll_name = self.term[0] + " - " + self.dt #set initial collection name

    def follow(self):# https://twitter.com/intent/user?user_id=XXX
        tmp = []
        print("Use http://gettwitterid.com to get a UID from a username. Must be a numeric value.")
        i = input("*Enter UID(s), separate with '||'. Leave blank for no user tracking, [r] - return/cancel.\n>>>").strip()
        if i == 'r':
            return
        self.users[:] = []  # clear list
        if i == '':
            return
        tmp = i.split('||')
        for i in range(len(tmp)):
            tmp[i] = tmp[i].replace(" ","")
            if tmp[i] == '' or not tmp[i].isdigit():  # if blank/not a num, dont append to search term list
                continue
            print("Verifying potential UID...")   #this could break if twitter changes their website
            try:
                if requests.get("https://twitter.com/intent/user?user_id=" + tmp[i]).status_code != 200:
                    if input("UID '" + tmp[i] + "' not found, attempt to follow anyway? [y/n]:").replace(" ","") == 'y':
                        self.users.append(tmp[i])
                else:
                    print("UID '" + tmp[i] + "' found!")
                    self.users.append(tmp[i])
            except requests.exceptions.ConnectionError:
                print("Connection failed. UID's will not be verified.")
                self.users.append(tmp[i])


def stream(search, lim, coll_name, db_name, temp, simil, lang, users):
    try:
        print("Initializing DB and Collection...")
        db = mongo.client[db_name]  # initialize db
        tweetcoll = db[coll_name]  # initialize collection
        if temp:
            tweetcoll.insert_one({ #This creates a coll even if no tweets found.
                "temp" : temp
            })
    except Exception as e:
        print("Error:",e)
        return
    while True: #start streaming
        try:
            listener = Listener(lim, tweetcoll, simil)
            print("Waiting for new tweets, press Ctrl+C to stop...")
            twitter_stream = Stream(auth, listener)
            twitter_stream.filter(track=search, languages=lang, follow=users) #location search is not a filter
        except KeyboardInterrupt:
            print("\n")
            break
        except IncompleteRead:
            print("Incomplete Read - Skipping to newer tweets.\n")
        except requests.exceptions.ConnectionError:
            print("Connection Failed - Check you internet.")
            return
        except Exception as e:
            print("Error: ",e,"\nAttempting to continue...\n")
            continue

if __name__ == '__main__':
    try:
        s = Setup()
        mongo.mongo_handler()
        s.search()
        #print("Collection: " + s.coll_name + ", Database: " + s.db_name)
        if mongo.connected:
            stream(s.term, s.limit(), s.coll_name, s.db_name, s.temp, s.sim, s.lang,s.users)
        else:
            print("MongoDB not connected/running. Cannot stream.")
    except BaseException as e:
        print("Error:",e)
    except KeyboardInterrupt:
        pass
