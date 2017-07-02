try:
    import mongo, datetime
except ImportError as e:
    print("Error:", e)
    quit()


class Setup:  # settings and setup for tweet scraping
    def __init__(self, streaming=False):
        self.streaming = streaming
        self.temp = False
        self.img = False
        self.lim = None
        self.db_name = 'twitter'
        self.lang = ['en']
        self.coll_name = str(self.get_dt())
        self.term = []
        self.users = []
        self.result_type = "mixed"
        self.before = None
        self.after = None

    def get_dt(self):
        return datetime.datetime.now()

    def set_date(self, inpt):
        self.before = None
        self.after = None

        def date_parse(text):
            id = text[0]
            del text[0]
            for i, k in enumerate(text):
                try:
                    text[i] = int(text[i])
                except ValueError as e:
                    print("Invalid Date!", e)
                    return
            try:
                valid_inpt = datetime.datetime(year=text[0], month=text[1], day=text[2])
                dt = self.get_dt()
                today = datetime.datetime(year=dt.year, month=dt.month, day=dt.day, hour=0, minute=0, second=0,
                                          microsecond=0)
                oldest = dt - datetime.timedelta(days=7, minutes=dt.minute, hours=dt.hour, seconds=dt.second,
                                                 microseconds=dt.microsecond)
                if valid_inpt < oldest:
                    print("Date is older than " + str(oldest) + ".")
                    return
                if valid_inpt > (today + datetime.timedelta(days=1)):
                    print("Date is in the future!")
                    return
                if id == 'A' or id == 'a':
                    self.after = valid_inpt.date()
                elif id == 'B' or id == 'b':
                    self.before = valid_inpt.date()
            except (ValueError, IndexError) as e:
                print("Invalid Date:", e)
                return

        inpt = inpt.split("||")
        first = inpt[0].split('-')
        if len(inpt) >= 2:
            second = inpt[1].split('-')
            date_parse(second)
        date_parse(first)
        if (self.before is not None and self.after is not None) and (
                self.before < self.after or self.before == self.after):
            print("'Before' date cannot be less than/equal to 'after' date.\n'Before' date removed.")
            self.before = None
        elif self.before is not None or self.after is not None:
            print("Date set" + ((" to on or after " + str(self.after)) if self.after is not None else "") + (
                (" to before " + str(self.before)) if self.before is not None else "") + ".")
        else:
            print("Date set to None.")

    def set_search(self, inpt):
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

    def set_follow(self, inpt):  # https://twitter.com/intent/user?user_id=XXX
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
            self.result_type = inpt

    def init_db(self):
        try:
            print("Initializing DB and Collection...")
            db = mongo.client[self.db_name]  # initialize db
            self.tweet_coll = db[self.coll_name]  # initialize collection
            self.tweet_coll.create_index([('text', 'text')])

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
        except Exception as e:
            print("Error:", e)
            return
