import mongo

class color:
    YELLOW = '\033[93m'
    BOLD = '\033[1m'
    END = '\033[0m'

def get_menu(menu, inpt_msg, items=None):
    while True:

        if menu is not None:
            print('-' * 40)
            for num,i in enumerate(menu):
                print("[" + color.YELLOW + str(num+1) + color.END + "] - " + i)

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
        if items is not None and i > items or i < 1:
            continue
        else:
            return i

def get_db():
    if not mongo.connected:
        print("You must be connected to MongoDB!")
        return
    print(color.YELLOW + "Do not select 'admin' or 'local' databases." + color.END)

    for j, k in enumerate(mongo.get_dbnames(), 1):  # start at 1
        print("[" + color.YELLOW + str(j) + color.END + "] - '" + k + "' (" + str(len(mongo.get_collections(k))) + ")") #print databases
    inpt = get_menu(None, "*Select a db to view collections or [r] - return.\n>>>", len(mongo.get_dbnames()))
    if inpt == 'r' or inpt == '':
        return None

    db = mongo.client[mongo.get_dbnames()[inpt - 1]]  # set up chosen db
    coll = mongo.get_collections(mongo.get_dbnames()[inpt - 1])  # collections list from that db
    return coll,db

def get_coll():
    try:
        coll,db = get_db()
    except:
        return None
    for j, k in enumerate(coll, 1):
        tmp = db[coll[j - 1]].find({"t_temp": True})
        doc_count = db[coll[j - 1]].find({})  # take the specified collection, and find all the documents
        print("[" + color.YELLOW + str(j) + color.END + "] - '" + k + "' (" + str(doc_count.count()) + ")" +
              ("(TEMP)" if tmp.count()>0 else ""))
        tmp.close()
        doc_count.close()
    inpt = get_menu(None, "*Select a collection or [r] - return.\n>>>", len(coll))

    if inpt == 'r' or inpt == '':
        return None
    return db[coll[inpt - 1]]
