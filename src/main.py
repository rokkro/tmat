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

        inpt = get_input(db_list, "Select a db to view collections.\n>>>", len(mongo.get_dbnames()))
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
                print("[" + str(j) + "] - '" + k + "' (" + str(doc_count.count()) + ")" + ("(temp)" if tmp.count()>0 else ""))

        inpt = get_input(coll_list, "Select a collection.\n>>>", len(coll))
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
        5: menu_list,
        6: menu_manage,
        7: mongo.mongo_handler
    }
    while True:
        i = get_input("[1] - Scrape tweets.\n"
          "[2] - Perform Sentiment Analysis.\n"
          "[3] - Perform Image Analysis.\n"
          "[4] - Data Presentation.\n"
          "[5] - List Databases and Collections.\n"
          "[6] - Manage Collections.\n"
          "[7] - MongoDB Connected = " + color.YELLOW + str(mongo.connected) + color.END,
                      "*Enter option number or [q] - quit.\n>>>", 7)
        try:
            menu[i]()
        except KeyError:
            pass
#############################
def menu_manage():
    selection = get_input("[1] - View Databases, Collections, and Documents.\n"
                          "[2] - Purge Temporary Collections in a DB.\n"
                          "[3] - Delete Specific Collections.\n"
                          "[4] - Mark a Collection as Temporary.\n"
                          "[5] - Unmark a Temporary Collection.",
                          "*Enter an option or [r] - return.\n>>>",5)

    def sub_tmp():
        deletable = []
        try:
            coll, db = get_list(True) #gets collection list and chosen db
        except:
            return
        print(color.YELLOW + "The following collections will be DELETED:" + color.END)
        for j, k in enumerate(coll, 1): #loops through all collections
            doc_count = db[coll[j - 1]].find({})  # take the current collection, and find all the documents
            cursor = db[coll[j - 1]].find({"temp":True})  #searches collection for doc with temp = True
            if cursor.count()>0: #if there's search results, then print the collection with temp = True
                print("'" + k + "' (" + str(doc_count.count()) + ")")
                deletable.append(db[coll[j-1]])
        selection = input(color.YELLOW + color.BOLD +"Are you sure you want to delete these collections and "
            "all documents within? [y/n]" + color.END + color.BOLD + "\n>>>" + color.END)
        if selection == 'y':
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
        selection = input(color.YELLOW + color.BOLD + "Are you sure you want to delete this collection and "
            "all documents within? [y/n]" + color.END + color.BOLD + "\n>>>" + color.END)
        if selection == 'y':
            coll.drop()
            print("Collection deleted.")
        else:
            print("Deletion canceled.")

        def sub_mark():
            '''
            coll = get_list()
            tmp = coll.find({"temp": True})
            coll.replace_one(
           {  # This creates a coll even if no tweets found. I may want to change this. Marks as tmp or not
                "temp": temp
           })
           '''

    menu = {
        1: menu_list,
        2: sub_tmp,
        3: sub_del,
    }
    menu[selection]()
###########################
def menu_list():
    i = get_list()
    if i==None:
        return
    cursor = i.find({})
    for j in cursor:
        print(j)

def menu_sentiment():
    selection = get_input("[1] - Run initial setup.\n[2] - Choose a collection to analyze.","Enter an option number or"
                                                                   " [r] -return.\n>>>",2)
    if selection=='r':
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
    menu[selection]()
########################
def menu_scrape():  # menu for setting up tweet scraping
    s = twitter.Setup()
    s.search()
    s.limit()
    while True:
        selection = get_input("[1] - Search = '" + str(s.term).strip('\'[]\'') + "'\n[2] - Limit = " + str(s.lim) +
            "\n[3] - Temporary Collection = " + str(s.temp) +
            "\n[4] - Database Name = '" + s.db_name + "'\n[5] - Collection Name = '" + s.coll_name +
            "'\n[6] - Tweet Similarity Threshold = " + str(s.sim) +
            "\n[7] - Languages = " + str(s.lang).strip('[]') +
            "\n[8] - MongoDB Connected = " + color.YELLOW + str(mongo.connected) + color.END,
            "*Enter option number or: [Enter] - begin if MongoDB is connected, [r] - return.""\n>>>", 8)

        if selection == '' and mongo.connected:
            twitter.stream(s.term, s.lim, s.coll_name, s.db_name, s.temp, s.sim, s.lang)
            break

        elif selection == '':
            continue

        elif selection == 'r':
            return

        def sub_search():
            s.search()
            print(color.YELLOW + "Search changed to '" + str(s.term).strip('\'[]\'') + "'." + color.END)

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
                inpt = input(color.BOLD + "Enter a new similarity threshold - 0.0 to 1.0. Higher value = filter out "
                    "higher similarity. Leave blank to cancel.\n>>>" + color.END)
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
            8: sub_mongo
        }
        menu[selection]()
########################

if __name__ == "__main__":
    try:
        menu_main()
    except KeyboardInterrupt:
        pass
