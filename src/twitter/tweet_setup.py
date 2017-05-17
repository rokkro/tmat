import mongo, datetime


class Setup:  # settings and setup for tweet scraping
    def __init__(self,streaming=False):
        self.streaming = streaming
        self.temp = False
        self.img = False
        self.lim = None
        self.db_name = 'twitter'
        self.sim = .55
        self.lang = ['en']
        self.coll_name = str(self.get_dt())
        self.term = []
        self.users = []
        self.result_type = "mixed"
        self.until = None

    def get_dt(self):
        return datetime.datetime.now()

    def set_date(self, inpt):
        inpt = inpt.split('-')
        for i, k in enumerate(inpt):
            try:
                inpt[i] = int(inpt[i])
            except ValueError:
                print("Invalid Date!")
                return
        try:
            valid = datetime.datetime(year=inpt[0], month=inpt[1], day=inpt[2])
            dt = self.get_dt()
            oldest = dt - datetime.timedelta(days=7,minutes=dt.minute,hours=dt.hour,seconds=dt.second,microseconds=dt.microsecond)
            if valid < oldest:
                print("Date is older than " + str(oldest) + ".")
                return
            self.until = valid.year + "-" + valid.month + "-" + valid.day
            print("Date set to " + str(self.until) + ".")
        except (ValueError, IndexError):
            print("Invalid Date.")
            return

    def set_search(self,inpt):
        tmp = []  # stores user input to filter out invalid responses
        self.term[:] = []
        if inpt == '':
            return
        tmp = inpt.split('||')  # split into list by ||
        for i in range(len(tmp)):
            tmp[i] = tmp[i].strip()  # remove outside spacing from all entries
            if tmp[i] == '':  # if blank after spaces removed, dont append to search term list
                continue
            self.term.append(tmp[i])
        if not self.term:  # if nothing appended to search term list, return.
            return
        self.coll_name = self.term[0] + " - " + str(self.get_dt())  # set initial collection name

    def set_follow(self,inpt):  # https://twitter.com/intent/user?user_id=XXX
        tmp = []
        self.users[:] = []  # clear list
        if inpt == '':  # if blank, then clear list beforehand
            return
        tmp = inpt.split('||')
        for i in range(len(tmp)):
            tmp[i] = tmp[i].replace(" ", "")
            if tmp[i] == '' or not tmp[i].isdigit():  # if blank/not a num, dont append to search term list
                continue
            self.users.append(tmp[i])

    def set_result_type(self, inpt):
        if inpt == 'mixed' or inpt == 'recent' or inpt == 'popular':
            self.result_type=inpt

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


