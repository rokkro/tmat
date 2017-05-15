import mongo, requests, datetime
from display import Color, get_menu

class Setup:  # settings and setup for tweet scraping
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

    def set_limit(self):
        inpt = get_menu(None, "*Enter number of tweets to retrieve. Leave blank for unlimited.\n>>>")
        if inpt == 'r':
            return
        if inpt == '':
            self.lim = None
        else:
            self.lim = inpt

    def set_search(self):
        tmp = []  # stores user input to filter out invalid responses
        i = input(Color.BOLD + "*Enter search term(s), separate multiple queries with '||'.\n>>>" + Color.END).strip()
        if i == 'r':
            return
        self.term[:] = []
        if i == '':
            self.coll_name = self.dt
            return
        tmp = i.split('||')  # split into list by ||
        for i in range(len(tmp)):
            tmp[i] = tmp[i].strip()  # remove outside spacing from all entries
            if tmp[i] == '':  # if blank after spaces removed, dont append to search term list
                continue
            self.term.append(tmp[i])
        if not self.term:  # if nothing appended to search term list, return.
            return
        self.coll_name = self.term[0] + " - " + self.dt  # set initial collection name

    def set_follow(self):  # https://twitter.com/intent/user?user_id=XXX
        tmp = []
        print("Use http://gettwitterid.com to get a UID from a username. Must be a numeric value.")
        i = input(Color.BOLD + "*Enter UID(s), separate with '||'. Leave blank for no user tracking, [r] - "
                               "return/cancel.\n>>>" + Color.END).strip()
        if i == 'r':
            return
        self.users[:] = []  # clear list
        if i == '':  # if blank, then clear list beforehand
            return
        tmp = i.split('||')
        for i in range(len(tmp)):
            tmp[i] = tmp[i].replace(" ", "")
            if tmp[i] == '' or not tmp[i].isdigit():  # if blank/not a num, dont append to search term list
                continue
            print("Verifying potential UID...")  # this could break if twitter changes their website
            try:
                if requests.get("https://twitter.com/intent/user?user_id=" + tmp[i]).status_code != 200:
                    if input("UID '" + tmp[i] + "' not found, attempt to follow anyway? [y/n]:").replace(" ",
                                                                                                         "") == 'y':
                        self.users.append(tmp[i])
                else:
                    print("UID '" + tmp[i] + "' found!")
                    self.users.append(tmp[i])
            except requests.exceptions.ConnectionError:
                print("Connection failed. UID's will not be verified.")
                self.users.append(tmp[i])

    def init_db(self):
        try:
            print("Initializing DB and Collection...")
            db = mongo.client[self.db_name]  # initialize db
            self.tweet_coll = db[self.coll_name]  # initialize collection
            c_true = self.tweet_coll.find({"t_temp": True})
            c_false = self.tweet_coll.find({"t_temp": False})
            doc_count = c_true.count() + c_false.count()

            if doc_count > 0:  # if there's already t_temp doc
                self.tweet_coll.update_many({"t_temp": not self.temp}, {'$set': {"t_temp": self.temp}})
            else:
                self.tweet_coll.insert_one({  # This creates a coll even if no tweets found.
                    "t_temp": self.temp
                })
            c_true.close()
            c_false.close()
        except BaseException as e:
            print("Error:", e)
            return


