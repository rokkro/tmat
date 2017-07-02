try:
    import mongo
except ImportError as e:
    print("Error",e)
class Menu:
    def __init__(self):
        self.purple = "\033[95m"
        self.cyan = '\033[36m'
        self.bold = '\033[1m'
        self.end = '\033[0m'
    
    def header(self,text):
        print(self.cyan + self.bold + ('-' * int((40 - len(text)) / 2)) + self.bold +
              text + self.cyan + self.bold + ('-' * int((40 - len(text)) / 2)) + self.end)
    
    def divider(self):
        print(self.cyan + self.bold + '-' * 40 + self.end)
    
    def get_menu(self,head, menu, input_menu):
        while True:
            if menu is not None:
                self.header(head)
                for num, i in enumerate(menu):
                    print("[" + self.purple + str(num + 1) + self.end + "] - " + i)
                self.divider()
            i = input(self.bold + input_menu.replace("[","[" + self.cyan).replace("]",self.end + "]") + self.end).replace(" ", "")
            if i == 'q':
                quit()
            elif i == 'r' or i == '':
                return i
            try:
                i = int(i)
            except ValueError:
                continue
            if ((i > len(menu)) if menu is not None else False) or i < 1:
                continue
            else:
                return i
    
    def get_db(self):
        if not mongo.connected:
            print(self.purple + "You must be connected to MongoDB!" + self.end)
            return
    
        print(self.purple + "Do not select 'admin' or 'local' databases." + self.end)
        db_list = []
        for j, k in enumerate(mongo.get_dbnames(), 1):  # start at 1
            db_list.append( k + "' (" + str(len(mongo.get_collections(k))) + ")")  # print databases
        inpt = self.get_menu("DATABASES",db_list, "*Select a db to view collections or [r] - return.\n>>>")
        if inpt == 'r' or inpt == '':
            return
    
        db = mongo.client[mongo.get_dbnames()[inpt - 1]]  # set up chosen db
        coll = mongo.get_collections(mongo.get_dbnames()[inpt - 1])  # collections list from that db
        return coll, db
    
    
    def get_coll(self):
        try:
            coll, db = self.get_db()
        except BaseException:
            return None
        coll_list = []
        for j, k in enumerate(coll, 1):
            tmp = db[coll[j - 1]].find({"t_temp": True})
            doc_count = db[coll[j - 1]].find({})  # take the specified collection, and find all the documents
            coll_list.append(k + "' (" + str(doc_count.count()) + ")" + ("(TEMP)" if tmp.count() > 0 else ""))
            tmp.close()
            doc_count.close()
        inpt = self.get_menu("COLLECTIONS",coll_list, "*Select a collection or [r] - return.\n>>>")
    
        if inpt == 'r' or inpt == '':
            return
        return db[coll[inpt - 1]]

    def mongo_connect(self):
        self.divider()
        print(self.purple, end='')
        mongo.mongo_connection()
        print(self.end, end='')
