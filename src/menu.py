try:
    import mongo
except ImportError as e:
    print("Error",e)

class Color:
    PURPLE = "\033[95m"
    CYAN = '\033[36m'
    BOLD = '\033[1m'
    END = '\033[0m'

def header(text):
    print(Color.CYAN  + Color.BOLD + ('-' * int((40 - len(text)) / 2)) + Color.BOLD +
          text + Color.CYAN + Color.BOLD + ('-' * int((40 - len(text)) / 2)) + Color.END)

def divider():
    print(Color.CYAN + Color.BOLD + '-' * 40 + Color.END)

def get_menu(head, menu, input_menu):
    while True:
        if menu is not None:
            header(head)
            for num, i in enumerate(menu):
                print("[" + Color.PURPLE + str(num + 1) + Color.END + "] - " + i)
            divider()
        i = input(Color.BOLD + input_menu + Color.END).replace(" ", "")
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

def get_db():
    if not mongo.connected:
        print(Color.PURPLE + "You must be connected to MongoDB!" + Color.END)
        return

    print(Color.PURPLE + "Do not select 'admin' or 'local' databases." + Color.END)
    db_list = []
    for j, k in enumerate(mongo.get_dbnames(), 1):  # start at 1
        db_list.append( k + "' (" + str(len(mongo.get_collections(k))) + ")")  # print databases
    inpt = get_menu("DATABASES",db_list, "*Select a db to view collections or [r] - return.\n>>>")
    if inpt == 'r' or inpt == '':
        return

    db = mongo.client[mongo.get_dbnames()[inpt - 1]]  # set up chosen db
    coll = mongo.get_collections(mongo.get_dbnames()[inpt - 1])  # collections list from that db
    return coll, db


def get_coll():
    try:
        coll, db = get_db()
    except BaseException:
        return None
    coll_list = []
    for j, k in enumerate(coll, 1):
        tmp = db[coll[j - 1]].find({"t_temp": True})
        doc_count = db[coll[j - 1]].find({})  # take the specified collection, and find all the documents
        coll_list.append(k + "' (" + str(doc_count.count()) + ")" + ("(TEMP)" if tmp.count() > 0 else ""))
        tmp.close()
        doc_count.close()
    inpt = get_menu("COLLECTIONS",coll_list, "*Select a collection or [r] - return.\n>>>")

    if inpt == 'r' or inpt == '':
        return
    return db[coll[inpt - 1]]
