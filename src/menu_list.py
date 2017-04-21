from display import color,get_coll,get_menu,get_db

def menu_manage():
    while True:
        inpt = get_menu("[1] - View Databases, Collections, and Documents.\n"
              "[2] - Purge Temporary Collections in a DB.\n"
              "[3] - Delete Specific Collections.\n"
              "[4] - Mark/Un-mark a Collection as Temporary.",
                "*Enter an option or [r] - return.\n>>>", 4)
        if inpt == 'r':
            return

        if inpt == '':
            continue

        def sub_list():
            i = get_coll()
            if i == None:
                return
            cursor = i.find({})
            for j in cursor:
                print(j)

        def sub_tmp():
            deletable = []
            try:
                coll, db = get_db() #gets collection list and chosen db
            except:
                return
            print(color.YELLOW + "The following collections will be DELETED:" + color.END)

            for j, k in enumerate(coll, 1): #loops through all collections
                doc_count = db[coll[j - 1]].find({})  # take the current collection, and find all the documents
                cursor = db[coll[j - 1]].find({"t_temp": True})  #searches collection for doc with temp = True
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
            coll = get_coll()
            if coll == None:
                return
            inpt = input(color.YELLOW + color.BOLD + "Are you sure you want to delete this collection and "
                "all documents within? [y/n]" + color.END + color.BOLD + "\n>>>" + color.END)
            if inpt == 'y':
                coll.drop()
                print("Collection deleted.")
            else:
                print("Deletion canceled.")

        def sub_mark(): #be careful if you manually added in other "temp" keys
            coll = get_coll()
            if coll == None:
                return
            c_true = coll.find({"t_temp": True})
            c_false = coll.find({"t_temp": False})
            if c_true.count()>0: #may want to reevaluate unique cases here, will flip any "temp" : True/False
                for i in c_true:
                    coll.replace_one({"t_temp": True},{"t_temp": False}) #safer to replace than delete
                print(color.YELLOW + "Collection marked as permanent." + color.END)
            elif c_false.count() > 0:
                for i in c_false:
                    coll.replace_one({"t_temp": False}, {"t_temp": True})
                print(color.YELLOW + "Collection marked as temporary." + color.END)
            else:
                coll.insert_one({"t_temp": True})
                print(color.YELLOW + "Collection marked as temporary." + color.END)

        menu = {
            1: sub_list,
            2: sub_tmp,
            3: sub_del,
            4: sub_mark,
        }
        try:
            menu[inpt]()
        except BaseException as e:
            print("Error:",e)
