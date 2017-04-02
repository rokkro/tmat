import mongo

class color:
    YELLOW = '\033[93m'
    BOLD = '\033[1m'
    END = '\033[0m'

def get_input(menu,inpt_msg, lim):
    while True:
        if menu is not None:
            print('-' * 40)
            print(menu)
        print('-' * 40)
        i = input(color.BOLD + inpt_msg + color.END).replace(" ","")
        if i == 'q':
            quit()
        elif i == 'r' or i == '':
            return i
        try:
            i = int(i)
        except ValueError:
            continue
        if i > lim or i < 1:
            continue
        else:
            return i

def get_list(db_only=False):
    if not mongo.connected:
        print("You must be connected to MongoDB!")
        return
    while True:
        print("Do not select 'admin' or 'local' databases.")
        def db_list():
            for j, k in enumerate(mongo.get_dbnames(), 1):  # start at 1
                print("[" + str(j) + "] - '" + k + "' (" + str(len(mongo.get_collections(k))) + ")")
        db_list()
        inpt = get_input(None,"Select a db to view collections or [r] - return.\n>>>", len(mongo.get_dbnames()))
        if inpt == 'r' or inpt == '':
            return None

        db = mongo.client[mongo.get_dbnames()[inpt - 1]]  # set up chosen db
        coll = mongo.get_collections(mongo.get_dbnames()[inpt - 1])  # collections list from that db

        if db_only:
            return coll,db

        def coll_list():
            for j, k in enumerate(coll, 1):
                tmp = db[coll[j - 1]].find({"temp": True})
                doc_count = db[coll[j - 1]].find({})  # take the specified collection, and find all the documents
                print("[" + str(j) + "] - '" + k + "' (" + str(doc_count.count()) + ")" +
                      ("(TEMP)" if tmp.count()>0 else ""))
        coll_list()
        inpt = get_input(None,"Select a collection or [r] - return.\n>>>", len(coll))
        if inpt == 'r' or inpt == '':
            continue
        return db[coll[inpt - 1]]