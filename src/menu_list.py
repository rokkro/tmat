from display import Color, get_coll, get_menu, get_db, header


def menu_manage():
    print("\n")
    while True:
        inpt = get_menu("MODIFY COLLECTIONS",["View Databases, Collections, and Documents.",
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
            if i is None:
                return
            cursor = i.find({})
            for j in cursor:
                print(j)
            cursor.close()

        def sub_tmp():
            deletable = []
            try:
                coll, db = get_db()  # gets collection list and chosen db
            except Exception:
                return
            print(Color.YELLOW + "The following collections will be DELETED:" + Color.END)

            for j, k in enumerate(coll, 1):  # loops through all collections
                doc_count = db[coll[j - 1]].find({}) # take the current collection, and find all the documents
                cursor = db[coll[j - 1]].find({"t_temp": True})  # searches collection for doc with t_temp = True
                if cursor.count() > 0:  # if there's search results, then print the collection with t_temp = True
                    print("'" + k + "' (" + str(doc_count.count()) + ")")
                    deletable.append(db[coll[j - 1]])
                doc_count.close()
                cursor.close()

            if not deletable: #if it's empty
                print(Color.YELLOW + "No temporary collections in this db." + Color.END)
                return
            inpt = input(Color.YELLOW + Color.BOLD + "Are you sure you want to delete these collections and "
                                                     "all documents within? [y/n]" + Color.END + Color.BOLD + "\n>>>" + Color.END)
            if inpt == 'y':
                for i in deletable:
                    i.drop()
                print(Color.YELLOW + "Temporary collections deleted." + Color.END)
            else:
                print(Color.YELLOW + "Deletion cancelled." + Color.END)

        def sub_del():
            print("Select a collection to delete.")
            coll = get_coll()
            if coll is None:
                return
            inpt = input(Color.YELLOW + Color.BOLD + "Are you sure you want to delete this collection and "
                                                     "all documents within? [y/n]" + Color.END + Color.BOLD + "\n>>>" + Color.END)
            if inpt == 'y':
                coll.drop()
                print(Color.YELLOW + "Collection deleted." + Color.END)
            else:
                print(Color.YELLOW + "Deletion canceled." + Color.END)

        def sub_mark():  # be careful if you manually added in other "temp" keys
            coll = get_coll()
            if coll is None:
                return
            c_true = coll.find({"t_temp": True})
            c_false = coll.find({"t_temp": False})
            if c_true.count() > 0:  # we will assume we want to flip any t_temp = trues
                coll.update_many({"t_temp": True}, {'$set': {"t_temp": False}})
                print(Color.YELLOW + "Collection marked as permanent." + Color.END)
            elif c_false.count() > 0:
                coll.update_many({"t_temp": False}, {'$set': {"t_temp": True}})
                print(Color.YELLOW + "Collection marked as temporary." + Color.END)
            else:
                coll.insert_one({  # This creates a coll even if no tweets found.
                    "t_temp": True
                })
                print(Color.YELLOW + "Collection marked as temporary." + Color.END)
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
            print("Error:", e)
