try:
    from mongo import Mongo
    from config import read_conf
except ImportError as e:
    print("Import Error in menu.py:",e)


class Menu(Mongo):
    notification_queue = []
    def __init__(self):
        self.horizontal_len = 40
        # Text colors
        self.colors = {
            "purple":"\033[1;94m",
            "cyan":'\033[36m',
            "end":'\033[1;0m',
        }
    
    def header(self,text): # ---header text---
        print(self.colors['end'] + self.colors['cyan'] + ('-' * int((self.horizontal_len - len(text)) / 2)) + self.colors['end'] +
              text + self.colors['end'] + self.colors['cyan'] + ('-' * int((self.horizontal_len - len(text)) / 2)) + self.colors['end'])

    def divider(self): # ----------
        print(self.colors['end'] + self.colors['cyan'] + '-' * self.horizontal_len + self.colors['end'])

    def notify(self,text):
        Menu.notification_queue.append(self.colors['purple'] + text + self.colors['end'])

    def notifications(self):
        if Menu.notification_queue:
            self.divider()
            print(self.colors['purple'] +  "\n".join(Menu.notification_queue) + self.colors['end'])
            Menu.notification_queue[:] = []

    def show_guide(self):
        # Suuper basic right now. Just sends notifications.
        self.notify("[r] - return to previous page")
        self.notify("[q] - quit the program")
        self.notify("[0] - reload settings file")
        self.notify("[?] - print this page")

    def get_menu(self,head, menu, input_menu):
        # Numbered user input menu
        while True:
            self.notifications()
            if menu is not None:
                self.header(head)
                for num, entry in enumerate(menu): # Print entries
                    print("[" + self.colors['purple'] + str(num + 1) + self.colors['end'] + "] - " + entry)
                self.divider()
            #Stylize input menu
            entry = input(self.colors['end'] + input_menu.replace("[", self.colors['end'] +
                                "[" + self.colors['purple']).replace("]",self.colors['end'] + "]" + self.colors['end'])).replace(" ", "")
            if entry == 'q': # input 'q' to quit
                quit()
            elif entry == '0':
                read_conf()
                self.notify("Reloaded config file.")
            elif entry == '?':
                self.show_guide()
            elif entry == 'r' or entry == '': # Returns r or space for menus to handle it.
                return entry
            try: # Type cast num input to int
                entry = int(entry)
            except ValueError:
                continue
            if ((entry > len(menu)) if menu is not None else False) or entry < 1:
                # (Compare entry to menu size if the menu exists, otherwise False) OR if input is < 1
                continue # Recognize as invalid input
            return entry # Successfully return input for menus to handle
    
    def get_db_menu(self):
        # Create menu to list Databases
        self.mongo_connection(True)
        if not self.is_connected():
            self.notify("You must be connected to MongoDB!")
            return

        self.notify("Do not select 'admin' or 'local' databases.")
        db_list = []
        for j, k in enumerate(self.get_db_names(), 1):  # start at 1
            db_list.append( k + "' (" + str(len(self.get_collections(k))) + ")")  # print databases
        inpt = self.get_menu("DATABASES",db_list, "*Select a db to view collections or [r] - return.\n>>>")
        if inpt == 'r' or inpt == '':
            return
    
        db = self.get_client()[self.get_db_names()[inpt - 1]]  # set up chosen db
        coll = self.get_collections(self.get_db_names()[inpt - 1])  # collections list from that db
        return coll, db
    
    def get_coll_menu(self):
        # Create menu to list collections
        try:
            coll, db = self.get_db_menu()
        except Exception:
            return None
        coll_list = []
        for iter, collection in enumerate(coll, 1):
            current_coll = db[coll[iter - 1]]
            tweet = current_coll.find({"t_type": "tweet"})
            speech = current_coll.find({"t_type": "speech"})
            tmp = current_coll.find({"t_temp": True})
            doc_count = current_coll.find({})  # take the specified collection, and find all the documents
            coll_list.append(collection + "' (" + str(doc_count.count()) + ")" + ("(TEMP)" if tmp.count() > 0 else "") +
                             ("(SPEECH)" if speech.count() > 0 else "") + ("(TWEET)" if tweet.count() > 0 else ""))
            tmp.close()
            tweet.close()
            speech.close()
            doc_count.close()
        inpt = self.get_menu("COLLECTIONS",coll_list, "*Select a collection or [r] - return.\n>>>")
    
        if inpt == 'r' or inpt == '':
            return
        return db[coll[inpt - 1]]

    def get_doc_menu(self, required, entry_name_key):
        # Create a menu for docs with 'transcript' and 'file_name' fields
        doc_list = []
        coll = self.get_coll_menu()
        if not coll:
            return None, None
        cursor = coll.find({})
        for doc in cursor:
            if not required:
                doc_list.append(doc)
                continue
            for enum, item in enumerate(required):
                if item not in doc:
                    break
                elif enum == len(required) - 1:
                    doc_list.append(doc)
        cursor.close()
        entries = []
        for doc in doc_list:
            try:
                entries.append(doc[entry_name_key])
            except KeyError:
                entries.append("(Unnamed)")

        inpt = self.get_menu("DOCS", entries, "*Select document to re-process text or [r] -return.\n>>>")
        if inpt == 'r' or not inpt:
            return None, None
        return coll, doc_list[inpt - 1]

    def mongo_connection(self, connect_only=False):
         if self.is_connected() and connect_only:
           return
         status = super().mongo_connection()
         if status is True:  # Returning an error == True with 'if status:'
            self.notify("*MongoDB Connection Succeeded!")
         elif not status:
             self.notify("*MongoDB Disconnected.")
         else:
             self.notify("*MongoDB Connection Failed:" + str(status))