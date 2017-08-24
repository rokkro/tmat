try:
    from twitter.tweet_setup import Setup
    from twitter.streaming import stream
    from twitter.historic import scrape
    from menu import Menu
except ImportError as e:
    print("Import Error in menu_twitter.py:", e)
    quit()


class MenuTwitter(Menu):
    def __init__(self,streaming=False):
        # Initialize Setup with streaming flag
        super().__init__()
        self.setup = Setup(streaming)

    def menu_stream(self):
        # Ugly streaming menu code.
        while True:
            str_search = str(self.setup.term).strip('[]') if self.setup.term else self.colors['purple'] + "None" + self.colors['end']
            str_uid = str(self.setup.users).strip('[]') if self.setup.users else self.colors['purple'] + "None" + self.colors['end']

            inpt = self.get_menu("STREAMING", ["Search = " + str_search ,
                "Limit = " + str(self.setup.lim),
                "Temporary Collection = " + str(self.setup.temp),
                "Database Name = '" + self.setup.db_name + "'",
                "Collection Name = '" + self.setup.coll_name + "'",
                "Languages = " + str(self.setup.lang).strip('[]'),
                "Follow UID(s) = " + str_uid,
                "MongoDB Connected = " + self.colors['purple'] + str(self.is_connected())],
                "*Enter option number or: [Enter] - start streaming, [r] - return.""\n>>>")

            if inpt == '' and self.is_connected() and (self.setup.term or self.setup.users):
                self.divider()
                print(self.colors['purple'], end='')
                self.setup.init_db(self.get_client())
                print("Waiting for new tweets...")
                print(self.colors['end'], end='')
                stream(self.setup)
                print("\n", end='')
                break
            elif inpt == '':
                self.notify("MongoDB must be connected and a search or UID must have been entered.")
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
                8: self.mongo_connection
            }
            menu[inpt]()

    def menu_hist(self):
        # Uglier historic menu code.
        while True:
            str_search = str(self.setup.term).strip('[]') if self.setup.term else self.colors['purple'] + "None" + self.colors['end']
            str_lim = (self.colors['purple'] + "None" + self.colors['end']) if self.setup.lim is None else str(self.setup.lim)
            str_date = ((("On/After " + str(self.setup.after) if self.setup.after is not None else "") +
                        ((", " if self.setup.after is not None and self.setup.before is not None else "") +
                      ("Before " + str(self.setup.before)) if self.setup.before is not None else ""))
                     if self.setup.after is not None or self.setup.before is not None else "None")

            inpt = self.get_menu("HISTORIC", ["Search = " + str_search,
                                  "Limit = " + str_lim,
                                  "Temporary Collection = " + str(self.setup.temp),
                                  "Database Name = '" + self.setup.db_name + "'",
                                  "Collection Name = '" + self.setup.coll_name + "'",
                                  "Result Type = " + self.setup.result_type,
                                  "Date Range = " + str_date,
                             "MongoDB Connected = " + self.colors['purple'] + str(self.is_connected()) + self.colors['end']],
                            "*Enter option number or: [Enter] - start streaming, [r] - return.""\n>>>")

            if inpt == '' and self.is_connected() and self.setup.term and self.setup.lim:
                self.divider()
                print(self.colors['purple'], end='')
                self.setup.init_db(self.get_client())
                print("Retrieving tweets...")
                print(self.colors['end'], end='')
                scrape(self.setup)
                print("\n", end='')
                break
            elif inpt == '':
                self.notify("MongoDB must be connected, and both a search and limit must have been entered.")
                continue

            menu = {
                1: self.sub_search,
                2: self.sub_lim,
                3: self.sub_tmp,
                4: self.sub_db,
                5: self.sub_coll,
                6: self.sub_result_type,
                7: self.sub_date,
                8: self.mongo_connection
            }
            menu[inpt]()

    def sub_search(self):
        # Sub menu for search input.
        if self.setup.streaming:
            print("*Enter search term(s), separate multiple queries with '||'.")
        else:
            print("*Enter search term(s), use https://dev.twitter.com/rest/public/search for operators.")
        inpt = input( self.colors['end'] +"*Leave blank to clear, [" + self.colors['cyan'] + "r" + self.colors['end'] + "] - return.\n>>>" + self.colors['end']).strip()
        if inpt == 'r':
            self.notify("Search unchanged.")
            return
        self.setup.set_search(inpt)
        self.notify("Search set to " + (
            str(self.setup.term).strip('[]') if self.setup.term else "None") + ".")

    def sub_lim(self):
        # Sub menu for limit input.
        if self.setup.streaming:
            print("*Enter number of tweets to retrieve. Leave blank for unlimited.",end='')
        else:
            print("*Enter number of tweets to retrieve.",end='')
        inpt = self.get_menu('',None, "\n>>>")
        if inpt == 'r':
            self.notify("Limit unchanged.")
            return
        if inpt == '':
            self.setup.lim = None
        else:
            self.setup.lim = inpt
        self.notify("Limit set to " + str(self.setup.lim) + ".")


    def sub_tmp(self):
        # Switches Setup().temp flag for temporary status.
        if not self.setup.temp:
            self.notify("Collection will be marked as Temporary.")
            self.setup.temp = True
        else:
            self.notify("Collection will be marked as Permanent.")
            self.setup.temp = False


    def sub_db(self):
        # Sub menu for inputting DB name.
        while True:
            inpt = input("Enter a new name for the database, currently '" + self.setup.db_name +
                         "'. Leave blank to cancel.\nSpaces and special characters will be removed.\n>>>" + self.colors['end'])
            inpt = ''.join(e for e in inpt if (e.isalnum() or e is "-"))
            if inpt == '' or inpt == self.setup.db_name or inpt == 'admin' or inpt == 'local':
                break
            self.notify("Database changed from '" + self.setup.db_name + "' to '" + inpt + "'.")
            self.setup.db_name = inpt
            if self.is_connected():
                if inpt in self.get_db_names():
                    self.notify("'" + inpt + "' already exists. New tweets will be added to existing.")
                else:
                    self.notify("New database '" + inpt + "' will be created.")
            break


    def sub_coll(self):
        # Sub menu for inputting collection name.
        while True:
            inpt = input(self.colors['end'] + "Enter a new name for this collection, currently '" + self.setup.coll_name +
                         "'. Leave blank to cancel.\nPut '[dt]' in name to insert date + time.\n>>>" +
                         self.colors['end']).strip().replace("$", "")
            if inpt == '' or inpt == self.setup.coll_name:  # If blank or collection name is same
                break
            if '[dt]' in inpt:  # inserting and replacing [dt] with date/time
                self.setup.coll_name = inpt.replace('[dt]', str(self.setup.get_dt())).strip()
            else:
                self.setup.coll_name = inpt
            self.notify("Collection changed to '" + self.setup.coll_name + "'.")
            if self.is_connected():
                if self.setup.coll_name in self.get_collections(self.setup.db_name):
                    self.notify("'" + self.setup.coll_name + "' already exists. New tweets will be added to existing.")
                else:
                    self.notify("New collection will be created.")
            break


    def sub_lang(self):
        # Sub menu for inputting streaming language setting.
        langs = ['en', 'ar', 'bn', 'cs', 'da', 'de', 'el', 'es', 'fa', 'fi', 'fil', 'fr', 'he', 'hi', 'hu', 'id',
                 'it',
                 'ja', 'ko', 'msa', 'nl', 'no', 'pl', 'pt', 'ro', 'ru', 'sv', 'th', 'tr', 'uk', 'ur', 'vl', 'zh-cn',
                 'zh-tw']
        inpt = input("Enter a comma separated list of language codes. "
                                  "https://dev.twitter.com/web/overview/languages\n>>>").replace(" ", '').split(',')
        if inpt == '':
            return
        tmp = []
        for i in inpt:
            if i in langs and i not in tmp:
                tmp.append(i)
        if len(tmp) >= 1:
            self.notify("Accepted languages: " + str(tmp).strip("[]") + ".")
            self.setup.lang = tmp

    def sub_result_type(self):
        self.setup.set_result_type()
        self.notify("Result type set to " + self.setup.result_type + ".")

    def sub_follow(self):
        # Sub menu for inputting streaming follower setting.
        print("Use http://gettwitterid.com to get a UID from a username. Must be a numeric value.")
        inpt = input("*Enter UID(s), separate with '||'. Leave blank for no user tracking, [" + self.colors['cyan'] +
                     "r" + self.colors['end'] + "] - return/cancel.\n>>>" + self.colors['end']).strip()
        if inpt == 'r':
            return
        self.setup.set_follow(inpt)
        self.notify("Follow list changed to " + (
            str(self.setup.users).strip('[]') if self.setup.users else "None") + ".")

    def sub_date(self):
        # Sub menu for setting 'before/after' date, see the README page for more information
        inpt = input(
             "*Enter cut off date(s). Must be: B/A-YYYY-MM-DD and no older than 7 days.\n"
                         "*B=Before (<), A=After (>=). Use '||' to separate.\n*Ex: 'b-2017-5-22||a-2017-5-20'. "
                         "Leave blank to clear, [" + self.colors['cyan'] + "r" + self.colors['end'] + "] - cancel.\n>>>" + self.colors['end'])
        inpt = inpt.strip().replace(" ", "")
        if inpt == "":
            self.setup.until = None
            self.setup.after = None
            return
        elif inpt == "r":
            return
        self.divider()
        print(self.colors['purple'], end="")
        self.setup.set_date(inpt)
        print(self.colors['end'], end="")
