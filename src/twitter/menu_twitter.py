try:
    import mongo
    from twitter.tweet_setup import Setup
    from twitter.streaming import stream
    from twitter.historic import scrape
    from menu import Menu
except ImportError as e:
    print("Error:", e)
    quit()


class MenuTwitter(Menu):
    def __init__(self,streaming=False):
        super().__init__()
        self.setup = Setup(streaming)

    def menu_stream(self):
        self.divider()
        self.sub_search()
        while True:
            inpt = self.get_menu("STREAMING", ["Search = " + (str(self.setup.term).strip('[]') if self.setup.term else "None"),
                                          "Limit = " + str(self.setup.lim),
                                          "Temporary Collection = " + str(self.setup.temp),
                                          "Database Name = '" + self.setup.db_name + "'",
                                          "Collection Name = '" + self.setup.coll_name + "'",
                                          "Languages = " + str(self.setup.lang).strip('[]'),
                                          "Follow UID(s) = " + (str(self.setup.users).strip('[]') if self.setup.users else "None"),
                                          "MongoDB Connected = " + self.PURPLE + str(mongo.connected) + self.END],
                            "*Enter option number or: [Enter] - start streaming, [r] - return.""\n>>>")

            if inpt == '' and mongo.connected and (self.setup.term or self.setup.users):
                self.divider()
                print(self.PURPLE, end='')
                print("Waiting for new tweets...")
                self.setup.init_db()
                print(self.END, end='')
                stream(self.setup)
                print("\n", end='')
                break
            elif inpt == '':
                print(self.PURPLE + "MongoDB must be connected and a search or UID must have been entered." + self.END)
                continue
            elif inpt == 'r':
                return

            menu = {
                1: self.sub_search,
                2: self.sub_lim,
                3: self.sub_tmp,
                4: self.sub_db,
                5: self.sub_coll,
                6: self.sub_lang,
                7: self.sub_follow,
                8: self.sub_connect
            }
            self.divider()
            menu[inpt]()

    def menu_hist(self):
        self.divider()
        self.sub_search()
        self.divider()
        self.sub_lim()
        while True:
            inpt = self.get_menu("HISTORIC", ["Search = " + (str(self.setup.term).strip('[]') if self.setup.term else "None"),
                                         "Limit = " + str(self.setup.lim),
                                         "Temporary Collection = " + str(self.setup.temp),
                                         "Database Name = '" + self.setup.db_name + "'",
                                         "Collection Name = '" + self.setup.coll_name + "'",
                                         "Result Type = " + self.setup.result_type,
                                         "Date Range = " + (
                                         (("On/After " + str(self.setup.after) if self.setup.after is not None else "") +
                                          ((", " if self.setup.after is not None and self.setup.before is not None else "") +
                                           ("Before " + str(self.setup.before)) if self.setup.before is not None else ""))
                                         if self.setup.after is not None or self.setup.before is not None else "None"),
                                         "MongoDB Connected = " + self.PURPLE + str(mongo.connected) + self.END],
                            "*Enter option number or: [Enter] - start streaming, [r] - return.""\n>>>")

            if inpt == '' and mongo.connected and self.setup.term and self.setup.lim:
                self.divider()
                print(self.PURPLE, end='')
                self.setup.init_db()
                print("Retrieving tweets...")
                print(self.END, end='')
                scrape(self.setup)
                print("\n", end='')
                break
            elif inpt == '':
                print(
                    self.PURPLE + "MongoDB must be connected, and both a search and limit must have been entered." + self.END)
                continue

            menu = {
                1: self.sub_search,
                2: self.sub_lim,
                3: self.sub_tmp,
                4: self.sub_db,
                5: self.sub_coll,
                6: self.sub_result,
                7: self.sub_date,
                8: self.sub_connect
            }
            self.divider()
            menu[inpt]()

    def sub_search(self):
        print(self.BOLD, end='')
        if self.setup.streaming:
            print(self.BOLD + "*Enter search term(s), separate multiple queries with '||'.")
        else:
            print(self.BOLD + "*Enter search term(s), use https://dev.twitter.com/rest/public/search for operators.")
        inpt = input("*Leave blank to clear, [r] - return.\n>>>" + self.END).strip()
        print(self.END,end='')
        self.divider()
        if inpt == 'r':
            return
        self.setup.set_search(inpt)
        print(self.END, end='')
        print(self.PURPLE + "Search set to " + (
            str(self.setup.term).strip('[]') if self.setup.term else "None") + "." + self.END)

    def sub_lim(self):
        print(self.BOLD, end='')
        if self.setup.streaming:
            print("*Enter number of tweets to retrieve. Leave blank for unlimited.",end='')
        else:
            print("*Enter number of tweets to retrieve.",end='')
        inpt = self.get_menu('',None, "\n>>>")
        self.divider()
        if inpt == 'r':
            return
        if inpt == '':
            self.setup.lim = None
        else:
            self.setup.lim = inpt
        print(self.END, end='')
        print(self.PURPLE + "Limit set to " + str(self.setup.lim) + "." + self.END)


    def sub_tmp(self):
        print(self.PURPLE, end='')
        if not self.setup.temp:
            print("Collection will be marked as Temporary.")
            self.setup.temp = True
        else:
            print("Collection will be marked as Permanent.")
            self.setup.temp = False
        print(self.END, end='')


    def sub_db(self):
        while True:
            inpt = input(self.BOLD + "Enter a new name for the database, currently '" + self.setup.db_name +
                         "'. Leave blank to cancel.\nSpaces and special characters will be removed.\n>>>" + self.END)
            inpt = ''.join(e for e in inpt if e.isalnum())
            if inpt == '' or inpt == self.setup.db_name or inpt == 'admin' or inpt == 'local':
                break
            self.divider()
            print(self.PURPLE + "Database changed from '" + self.setup.db_name + "' to '" + inpt + "'.")
            self.setup.db_name = inpt
            if mongo.connected:
                if inpt in mongo.get_dbnames():
                    print("'" + inpt + "' already exists. New tweets will be added to existing.")
                else:
                    print("New database '" + inpt + "' will be created.")
            print(self.END, end='')
            break


    def sub_coll(self):
        while True:
            inpt = input(self.BOLD + "Enter a new name for this collection, currently '" + self.setup.coll_name +
                         "'. Leave blank to cancel.\nPut '[dt]' in name to insert date + time.\n>>>" +
                         self.END).strip().replace("$", "")
            if inpt == '' or inpt == self.setup.coll_name:  # If blank or collection name is same
                break
            if '[dt]' in inpt:  # inserting and replacing [dt] with date/time
                self.setup.coll_name = inpt.replace('[dt]', str(self.setup.get_dt())).strip()
            else:
                self.setup.coll_name = inpt
            self.divider()
            print(self.PURPLE + "Collection changed to '" + self.setup.coll_name + "'.")
            if mongo.connected:
                if self.setup.coll_name in mongo.get_collections(self.setup.db_name):
                    print("'" + self.setup.coll_name + "' already exists. New tweets will be added to existing.")
                else:
                    print("New collection will be created.")
            print(self.END, end='')
            break


    def sub_lang(self):
        langs = ['en', 'ar', 'bn', 'cs', 'da', 'de', 'el', 'es', 'fa', 'fi', 'fil', 'fr', 'he', 'hi', 'hu', 'id',
                 'it',
                 'ja', 'ko', 'msa', 'nl', 'no', 'pl', 'pt', 'ro', 'ru', 'sv', 'th', 'tr', 'uk', 'ur', 'vl', 'zh-cn',
                 'zh-tw']
        inpt = input(self.BOLD + "Enter a comma separated list of language codes. "
                                  "https://dev.twitter.com/web/overview/languages\n>>>").replace(" ", '').split(',')
        if inpt == '':
            return
        self.divider()
        tmp = []
        for i in inpt:
            if i in langs and i not in tmp:
                tmp.append(i)
        if len(tmp) >= 1:
            print(self.PURPLE + "Accepted languages: " + str(tmp).strip("[]") + "." + self.END)
            self.setup.lang = tmp


    def sub_follow(self):
        print(self.BOLD, end='')
        print("Use http://gettwitterid.com to get a UID from a username. Must be a numeric value.")
        inpt = input(self.BOLD + "*Enter UID(s), separate with '||'. Leave blank for no user tracking, [r] - "
                               "return/cancel.\n>>>" + self.END).strip()
        if inpt == 'r':
            return
        self.divider()
        self.setup.set_follow(inpt)
        print(self.END, end='')
        print(self.PURPLE + "Follow list changed to " + (
            str(self.setup.users).strip('[]') if self.setup.users else "None") + "." + self.END)

    def sub_result(self):
        inpt = input(self.BOLD + "*Enter a result type: 'mixed','recent', or 'popular'.\n>>>" + self.END).strip()
        self.setup.set_result_type(inpt)
        print(self.PURPLE + "Result type set to " + self.setup.result_type + "." + self.END)

    def sub_date(self):
        inpt = input(
            self.BOLD + "*Enter cut off date(s). Must be: B/A-YYYY-MM-DD and no older than 7 days.\n"
                         "*B=Before (<), A=After (>=). Use '||' to separate.\n*Ex: 'b-2017-5-22||a-2017-5-20'. "
                         "Leave blank to clear, [r] - cancel.\n>>>" + self.END)
        inpt = inpt.strip().replace(" ", "")
        if inpt == "":
            self.setup.until = None
            self.setup.after = None
            return
        elif inpt == "r":
            return
        self.divider()
        print(self.PURPLE, end="")
        self.setup.set_date(inpt)
        print(self.END,end="")


