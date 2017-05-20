try:
    import mongo
except ImportError as e:
    print("Error",e)

class Color:
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

def header(text):
    print(Color.CYAN  + Color.BOLD + ('-' * int((40 - len(text)) / 2)) + Color.BOLD +
          text + Color.CYAN + Color.BOLD + ('-' * int((40 - len(text)) / 2)) + Color.END)
def footer():
    print(Color.CYAN + Color.BOLD + '-' * 40 + Color.END)

def get_menu(head,menu, inpt_msg, items=None):
    while True:
        if menu is not None:
            header(head)
            for num, i in enumerate(menu):
                print("[" + Color.YELLOW + str(num + 1) + Color.END + "] - " + i)
            footer()
        i = input(Color.BOLD + inpt_msg + Color.END).replace(" ", "")
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
        print(Color.YELLOW + "You must be connected to MongoDB!" + Color.END)
        return

    header("DATABASES")
    print(Color.YELLOW + "Do not select 'admin' or 'local' databases." + Color.END)

    for j, k in enumerate(mongo.get_dbnames(), 1):  # start at 1
        print("[" + Color.YELLOW + str(j) + Color.END + "] - '" + k + "' (" + str(
            len(mongo.get_collections(k))) + ")")  # print databases
    footer()
    inpt = get_menu("",None, "*Select a db to view collections or [r] - return.\n>>>", len(mongo.get_dbnames()))
    if inpt == 'r' or inpt == '':
        return None

    db = mongo.client[mongo.get_dbnames()[inpt - 1]]  # set up chosen db
    coll = mongo.get_collections(mongo.get_dbnames()[inpt - 1])  # collections list from that db
    return coll, db


def get_coll():
    try:
        coll, db = get_db()
    except BaseException:
        return None
    header("COLLECTIONS")
    for j, k in enumerate(coll, 1):
        tmp = db[coll[j - 1]].find({"t_temp": True})
        doc_count = db[coll[j - 1]].find({})  # take the specified collection, and find all the documents
        print("[" + Color.YELLOW + str(j) + Color.END + "] - '" + k + "' (" + str(doc_count.count()) + ")" +
              ("(TEMP)" if tmp.count() > 0 else ""))
        tmp.close()
        doc_count.close()
    footer()
    inpt = get_menu("",None, "*Select a collection or [r] - return.\n>>>", len(coll))

    if inpt == 'r' or inpt == '':
        return None
    return db[coll[inpt - 1]]
