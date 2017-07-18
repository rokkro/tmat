try:
    from menu import Menu
    import mongo
except ImportError as e:
    print("Import Error in menu_manage.py:",e)


class MenuManage(Menu):
    def __init__(self):
        super().__init__()

    def menu_manage(self):
        menu = {
            1: self.sub_list,
            2: self.sub_tmp,
            3: self.sub_del_coll,
            4: self.sub_del_db,
            5: self.sub_mark,
            6: self.sub_strip_sentiment,
            7: self.sub_strip_read,
            8: self.sub_strip_facial
        }
        while True:
            inpt = self.get_menu("MANAGE COLLECTIONS", ["View Databases, Collections, and Documents.",
                                                        "Purge Temporary Collections in a DB.",
                                                        "Delete a Collection.",
                                                        "Delete a Database.",
                                                        "Mark/Un-mark a Collection as Temporary.",
                                                        "Remove Sentiment Values.",
                                                        "Remove Readability Values.",
                                                        "Remove Facial Analysis Values."],
                                 "*Enter an option or [r] - return.\n>>>")

            if inpt == 'r':
                return

            if inpt == '':
                continue

            try:
                print(self.purple, end='')
                menu[inpt]()
            except Exception as e:
                print("Error in menu_manage.py:", e)

    def sub_list(self):
        # Print documents
        inpt = self.get_coll_menu()
        if inpt is None:
            return
        cursor = inpt.find({})
        for doc in cursor:
            print(doc)
        cursor.close()

    def sub_tmp(self):
        # Delete temp collection
        deletable = []
        try:
            coll, db = self.get_db_menu()  # gets collection list and chosen db
        except Exception:
            return
        self.divider()
        print(self.purple + "The following collections will be DELETED:" + self.end)

        for num, item in enumerate(coll, 1):  # loops through all collections
            doc_count = db[coll[num - 1]].find({}) # take the current collection, and find all the documents
            cursor = db[coll[num - 1]].find({"t_temp": True})  # searches collection for doc with t_temp = True
            if cursor.count() > 0:  # if there's search results, then print the collection with t_temp = True
                print("'" + item + "' (" + str(doc_count.count()) + ")")
                deletable.append(db[coll[num - 1]])
            doc_count.close()
            cursor.close()

        if not deletable: #if it's empty
            print(self.purple + "No temporary collections in this db." + self.end)
            return
        inpt = input(self.purple+ "Are you sure you want to delete these collections and "
                                                 "all documents within? [y/n]" + self.end + "\n>>>" + self.end)
        if inpt == 'y':
            for i in deletable:
                i.drop()
            print(self.purple + "Temporary collections deleted." + self.end)
        else:
            print(self.purple + "Deletion cancelled." + self.end)

    def sub_del_coll(self):
        # Delete specified collection
        coll = self.get_coll_menu()
        if coll is None:
            return
        inpt = input(self.purple +  "Are you sure you want to delete this collection and "
                                                 "all documents within? [y/n]" + self.end + "\n>>>" + self.end)
        self.divider()
        if inpt == 'y':
            coll.drop()
            print(self.purple + "Collection deleted." + self.end)
        else:
            print(self.purple + "Deletion canceled." + self.end)

    def sub_del_db(self):
        # Delete specified database
        try:
            client = mongo.get_client()
            coll, db = self.get_db_menu()
        except TypeError as e:
            return

        inpt = input(self.purple + "Are you sure you want to delete this database and "
                                   "collections and documents within? [y/n]" + self.end + "\n>>>" + self.end)
        self.divider()
        if inpt == 'y':
            client.drop_database(db)
            print(self.purple + "Database deleted." + self.end)
        else:
            print(self.purple + "Deletion canceled." + self.end)

    def sub_mark(self):
        # Mark/unmark a collection as temporary
        coll = self.get_coll_menu()
        if coll is None:
            return
        self.divider()
        c_true = coll.find({"t_temp": True})
        c_false = coll.find({"t_temp": False})
        if c_true.count() > 0:  # we will assume we want to flip any t_temp = trues
            coll.update_many({"t_temp": True}, {'$set': {"t_temp": False}})
            print(self.purple + "Collection marked as permanent." + self.end)
        elif c_false.count() > 0:
            coll.update_many({"t_temp": False}, {'$set': {"t_temp": True}})
            print(self.purple + "Collection marked as temporary." + self.end)
        else:
            coll.insert_one({  # This creates a coll even if no tweets found.
                "t_temp": True
            })
            print(self.purple + "Collection marked as temporary." + self.end)
        c_true.close()
        c_false.close()

    def sub_strip_sentiment(self):
        # Remove sentiment values
        coll = self.get_coll_menu()
        if coll is None:
            return
        self.divider()
        coll.update({},{"$unset":{"sentiment":1}},multi=True)
        print(self.purple + "Sentiment values have been removed." + self.end)

    def sub_strip_read(self):
        # Remove reading values
        coll = self.get_coll_menu()
        if coll is None:
            return
        self.divider()
        coll.update({},{"$unset":{"readability":1}},multi=True)
        print(self.purple + "Readability values have been removed." + self.end)

    def sub_strip_facial(self):
        # Remove kairos values
        coll = self.get_coll_menu()
        if coll is None:
            return
        self.divider()
        coll.update({},{"$unset":{"face":1}},multi=True)
        print(self.purple + "Facial analysis values have been removed." + self.end)
