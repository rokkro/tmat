import twitter, mongo, sentiment

class color:
    YELLOW = '\033[93m'
    BOLD = '\033[1m'
    END = '\033[0m'

def get_input(msg, inpt_msg, lim):
    while True:
        print(len(inpt_msg) * '-')
        if type(msg) is str:
            print(msg)
        else:
            msg()
        print(len(inpt_msg) * '-')
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
        def db_list():
            for j, k in enumerate(mongo.get_dbnames(), 1):  # start at 1
                print("[" + str(j) + "] - '" + k + "' (" + str(len(mongo.get_collections(k))) + ")")

        inpt = get_input(db_list, "Select a db to view collections or [r] - return.\n>>>", len(mongo.get_dbnames()))
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

        inpt = get_input(coll_list, "Select a collection or [r] - return.\n>>>", len(coll))
        if inpt == 'r' or inpt == '':
            continue
        return db[coll[inpt - 1]]

def menu_main():
    print(color.YELLOW, end='')
    mongo.mongo_handler()
    print(color.END, end='')
    menu = {
        1: menu_scrape,
        2: menu_sentiment,
        3: exit,
        4: exit,
        5: menu_manage,
        6: mongo.mongo_handler
    }
    while True:
        i = get_input("[1] - Scrape tweets.\n"
          "[2] - Perform Sentiment Analysis.\n"
          "[3] - Perform Image Analysis.\n"
          "[4] - Data Presentation.\n"
          "[5] - Manage Collections.\n"
          "[6] - MongoDB Connected = " + color.YELLOW + str(mongo.connected) + color.END,
                      "*Enter option number or [q] - quit.\n>>>", 7)
        try:
            menu[i]()
        except KeyError:
            pass
#############################
def menu_manage():
    while True:
        inpt = get_input("[1] - View Databases, Collections, and Documents.\n"
                              "[2] - Purge Temporary Collections in a DB.\n"
                              "[3] - Delete Specific Collections.\n"
                              "[4] - Mark/Un-mark a Collection as Temporary.",
                              "*Enter an option or [r] - return.\n>>>",4)

        def sub_list():
            i = get_list()
            if i == None:
                return
            cursor = i.find({})
            for j in cursor:
                print(j)

        def sub_tmp():
            deletable = []
            try:
                coll, db = get_list(True) #gets collection list and chosen db
            except:
                return
            print(color.YELLOW + "The following collections will be DELETED:" + color.END)
            for j, k in enumerate(coll, 1): #loops through all collections
                doc_count = db[coll[j - 1]].find({})  # take the current collection, and find all the documents
                cursor = db[coll[j - 1]].find({"temp": True})  #searches collection for doc with temp = True
                if cursor.count()>0: #if there's search results, then print the collection with temp = True
                    print("'" + k + "' (" + str(doc_count.count()) + ")")
                    deletable.append(db[coll[j-1]])
            if len(deletable) == 0:
                print(color.YELLOW + "No temporary collections in this db." + color.END)
                return
            inpt = input(color.YELLOW + color.BOLD +"Are you sure you want to delete these collections and "
                "all documents within? [y/n]" + color.END + color.BOLD + "\n>>>" + color.END)
            if inpt == 'y':
              for i in deletable:
                  i.drop()
              print("Temporary collections deleted.")
            else:
              print("Deletion cancelled.")

        def sub_del():
            print("Select a collection to delete.")
            coll = get_list()
            if coll == None:
                return
            inpt = input(color.YELLOW + color.BOLD + "Are you sure you want to delete this collection and "
                "all documents within? [y/n]" + color.END + color.BOLD + "\n>>>" + color.END)
            if inpt == 'y':
                coll.drop()
                print("Collection deleted.")
            else:
                print("Deletion canceled.")

        def sub_mark(): #be careful if you manually added in "temp" keys
            coll = get_list()
            if coll == None:
                return
            c_true = coll.find({"temp": True})
            c_false = coll.find({"temp": False})
            if c_true.count()>0: #may want to reevaluate unique cases here, will flip any "temp" : True/False
                for i in c_true:
                    coll.replace_one({"temp": True},{"temp": False}) #safer to replace than delete
                print(color.YELLOW + "Collection marked as permanent." + color.END)
            elif c_false.count() > 0:
                for i in c_false:
                    coll.replace_one({"temp": False}, {"temp": True})
                print(color.YELLOW + "Collection marked as temporary." + color.END)
            else:
                coll.insert_one({"temp": True})
                print(color.YELLOW + "Collection marked as temporary." + color.END)

        menu = {
            1: sub_list,
            2: sub_tmp,
            3: sub_del,
            4: sub_mark,
        }
        menu[inpt]()
########################
def menu_sentiment():
    inpt = get_input("[1] - Run initial setup.\n[2] - Choose a collection to analyze.","Enter an option number or"
                                                                   " [r] - return.\n>>>",2)
    if inpt=='r':
        return

    def sub_analysis():
        i = get_list()
        if i==None:
            return
        sentiment.analyze(i)

    menu = {
        1:sentiment.initialize,
        2:sub_analysis,
    }
    menu[inpt]()
########################
def menu_scrape():  # menu for setting up tweet scraping
    s = twitter.Setup()
    s.search()
    while True:
        inpt = get_input("[1] - Search = " + (str(s.term).strip('[]') if len(s.term) > 0 else "None") +
            "\n[2] - Limit = " + str(s.lim) +
            "\n[3] - Temporary Collection = " + str(s.temp) +
            "\n[4] - Database Name = '" + s.db_name + "'\n[5] - Collection Name = '" + s.coll_name +
            "'\n[6] - Tweet Similarity Threshold = " + str(s.sim) +
            "\n[7] - Languages = " + str(s.lang).strip('[]') +
            "\n[8] - Follow UID(s) = " + (str(s.users).strip('[]') if len(s.users) > 0 else "None") +
            "\n[9] - MongoDB Connected = " + color.YELLOW + str(mongo.connected) + color.END,
            "*Enter option number or: [Enter] - start streaming or [r] - return.""\n>>>", 9)

        if inpt == '' and mongo.connected and (len(s.term)>0 or len(s.users)>0):
            twitter.stream(s.term, s.lim, s.coll_name, s.db_name, s.temp, s.sim, s.lang, s.users)
            break
        elif inpt == '':
            print(color.YELLOW + "MongoDB must be connected and a search or UID must have been entered." + color.END)
            continue

        elif inpt == 'r':
            return

        def sub_search():
            s.search()
            print(color.YELLOW + "Search changed to " +(str(s.term).strip('[]') if len(s.term) > 0 else "None") + "." + color.END)

        def sub_lim():
            s.limit()
            print(color.YELLOW + "Limit changed to " + str(s.lim) + "." + color.END)

        def sub_tmp():
            print(color.YELLOW, end='')
            if s.temp == False:
                print("Collection will be marked as Temporary.")
                s.temp = True
            else:
                print("Collection will be marked as Permanent.")
                s.temp = False
            print(color.END, end='')

        def sub_db():
            while True:
                inpt = input(color.BOLD + "Enter a new name for the database, currently '" + s.db_name +
                    "'. Leave blank to cancel. ""Spaces and special characters will be removed.\n>>>" + color.END)
                inpt = ''.join(e for e in inpt if e.isalnum())
                if inpt == '' or inpt == s.db_name or inpt == 'admin' or inpt == 'local':
                    break
                print(color.YELLOW + "Database changed from '" + s.db_name + "' to '" + inpt + "'.")
                s.db_name = inpt
                if mongo.connected:
                    if inpt in mongo.get_dbnames():
                        print("'" + inpt + "' already exists. New tweets will be added to existing.")
                    else:
                        print("New database '" + inpt + "' will be created.")
                print(color.END, end='')
                break

        def sub_coll():
            while True:
                inpt = input(color.BOLD + "Enter a new name for this collection, currently '" + s.coll_name +
                    "'. Leave blank to cancel.\nPut '[dt]' in name to insert date + time.\n>>>" +
                             color.END).strip().replace("$","")
                if inpt == '' or inpt == s.coll_name:  # If blank or collection name is same
                    break
                if '[dt]' in inpt:  # inserting and replacing [dt] with date/time
                    s.coll_name = inpt.replace('[dt]', s.dt).strip()
                else:
                    s.coll_name = inpt
                print(color.YELLOW + "Collection changed to '" + s.coll_name + "'.")
                if mongo.connected:
                    if s.coll_name in mongo.get_collections(s.db_name):
                        print("'" + s.coll_name + "' already exists. New tweets will be added to existing.")
                    else:
                        print("New collection will be created.")
                print(color.END, end='')
                break

        def sub_simil():
            while True:
                inpt = input(color.BOLD + "Enter a new simil threshold - 0.0 to 1.0. Higher value = filter out "
                    "higher simil. Leave blank to cancel.\n>>>" + color.END)
                if inpt == '' or inpt == s.sim:
                    break
                try:
                    inpt = float(inpt)
                    if inpt <= 1.0 and inpt >= 0:
                        s.sim = inpt
                    else:
                        raise ValueError
                    print(color.YELLOW + "Similarity threshold set to " + str(s.sim) + "." + color.END)
                    break
                except ValueError:
                    print("Invalid Input.")
                    continue

        def sub_lang():
            langs = ['en','ar','bn','cs','da','de','el','es','fa','fi','fil','fr','he','hi','hu','id','it',
                     'ja','ko','msa','nl','no','pl','pt','ro','ru','sv','th','tr','uk','ur','vl','zh-cn','zh-tw']
            inpt = input(color.BOLD + "Enter a comma separated list of language codes. "
                "https://dev.twitter.com/web/overview/languages\n>>>").replace(" ",'').split(',')
            if inpt == '':
                return
            tmp = []
            for i in inpt:
                if i in langs and i not in tmp:
                    tmp.append(i)
            if len(tmp) >=1:
                print(color.YELLOW + "Accepted languages: " + str(tmp).strip("[]") + "." + color.END)
                s.lang = tmp

        def sub_follow():
            s.follow()
            print(color.YELLOW + "Follow list changed to " + (str(s.users).strip('[]') if len(s.users) > 0 else "None") + "." + color.END)

        def sub_mongo():
            print(color.YELLOW, end='')
            mongo.mongo_handler()
            print(color.END, end='')

        menu = {
            1: sub_search,
            2: sub_lim,
            3: sub_tmp,
            4: sub_db,
            5: sub_coll,
            6: sub_simil,
            7: sub_lang,
            8: sub_follow,
            9: sub_mongo
        }
        menu[inpt]()
########################

if __name__ == "__main__":
    try:
        menu_main()
    except KeyboardInterrupt:
        pass
