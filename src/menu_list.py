from display import color,get_coll,get_menu,get_db

def menu_manage():
    while True:
        inpt = get_menu(["View Databases, Collections, and Documents.",
              "Purge Temporary Collections in a DB.",
              "Delete Specific Collections.",
              "Mark/Un-mark a Collection as Temporary."],
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
            cursor.close()

        def sub_tmp():
            deletable = []
            try:
                coll, db = get_db() #gets collection list and chosen db
            except:
                return
            print(color.YELLOW + "The following collections will be DELETED:" + color.END)

            for j, k in enumerate(coll, 1): #loops through all collections
                doc_count = db[coll[j - 1]].find({})  # take the current collection, and find all the documents
                cursor = db[coll[j - 1]].find({"t_temp": True})  #searches collection for doc with t_temp = True
                if cursor.count()>0: #if there's search results, then print the collection with t_temp = True
                    print("'" + k + "' (" + str(doc_count.count()) + ")")
                    deletable.append(db[coll[j-1]])
                doc_count.close()
                cursor.close()

            if len(deletable) == 0:
                print(color.YELLOW + "No temporary collections in this db." + color.END)
                return
            inpt = input(color.YELLOW + color.BOLD +"Are you sure you want to delete these collections and "
                "all documents within? [y/n]" + color.END + color.BOLD + "\n>>>" + color.END)
            if inpt == 'y':
              for i in deletable:
                  i.drop()
              print(color.YELLOW + "Temporary collections deleted." + color.END)
            else:
              print(color.YELLOW + "Deletion cancelled." + color.END)

        def sub_del():
            print("Select a collection to delete.")
            coll = get_coll()
            if coll == None:
                return
            inpt = input(color.YELLOW + color.BOLD + "Are you sure you want to delete this collection and "
                "all documents within? [y/n]" + color.END + color.BOLD + "\n>>>" + color.END)
            if inpt == 'y':
                coll.drop()
                print(color.YELLOW + "Collection deleted." + color.END)
            else:
                print(color.YELLOW + "Deletion canceled." + color.END)

        def sub_mark(): #be careful if you manually added in other "temp" keys
            coll = get_coll()
            if coll == None:
                return
            c_true = coll.find({"t_temp":True})
            c_false = coll.find({"t_temp":False})
            if c_true.count() > 0: #we will assume we want to flip any t_temp = trues moreso if there are multiple t_temps
                coll.update_many({"t_temp": True}, {'$set': {"t_temp": False}})
                print(color.YELLOW + "Collection marked as permanent." + color.END)
            elif c_false.count() > 0:
                coll.update_many({"t_temp": False}, {'$set': {"t_temp": True}})
                print(color.YELLOW + "Collection marked as temporary." + color.END)
            else:
                coll.insert_one({  # This creates a coll even if no tweets found.
                    "t_temp": True
                })
                print(color.YELLOW + "Collection marked as temporary." + color.END)
            c_true.close()
            c_false.close()

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
