try:
    from menu import Menu
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
                menu[inpt]()
            except Exception as e:
                Menu.notification_queue.append("Error in menu_manage.py:" + str(e))

    def sub_list(self):
        # Print documents
        inpt = self.get_coll_menu()
        if inpt is None:
            return
        cursor = inpt.find({})
        for doc in cursor:
            Menu.notification_queue.append(str(doc))
        cursor.close()

    def sub_tmp(self):
        # Delete temp collection
        deletable = []
        try:
            coll, db = self.get_db_menu()  # gets collection list and chosen db
        except Exception:
            return
        self.divider()
        print(self.colors['purple'] + "The following collections will be DELETED:" + self.colors['end'])

        for num, item in enumerate(coll, 1):  # loops through all collections
            doc_count = db[coll[num - 1]].find({}) # take the current collection, and find all the documents
            cursor = db[coll[num - 1]].find({"t_temp": True})  # searches collection for doc with t_temp = True
            if cursor.count() > 0:  # if there's search results, then print the collection with t_temp = True
                print("'" + item + "' (" + str(doc_count.count()) + ")")
                deletable.append(db[coll[num - 1]])
            doc_count.close()
            cursor.close()

        if not deletable: #if it's empty
            Menu.notification_queue.append("No temporary collections in this db.")
            return
        inpt = input(self.colors['purple']+ "Are you sure you want to delete these collections and "
                                                 "all documents within? [y/n]" + self.colors['end'] + "\n>>>" + self.colors['end'])
        if inpt == 'y':
            for i in deletable:
                i.drop()
                Menu.notification_queue.append("Temporary collections deleted.")
        else:
            Menu.notification_queue.append("Deletion cancelled.")

    def sub_del_coll(self):
        # Delete specified collection
        coll = self.get_coll_menu()
        if coll is None:
            return
        inpt = input(self.colors['purple'] +  "Are you sure you want to delete this collection and "
                                                 "all documents within? [y/n]" + self.colors['end'] + "\n>>>" + self.colors['end'])
        if inpt == 'y':
            coll.drop()
            Menu.notification_queue.append("Collection deleted.")
        else:
            Menu.notification_queue.append("Deletion canceled.")

    def sub_del_db(self):
        # Delete specified database
        try:
            client = self.get_client()
            coll, db = self.get_db_menu()
        except TypeError as e:
            return

        inpt = input(self.colors['purple'] + "Are you sure you want to delete this database and "
                                   "collections and documents within? [y/n]" + self.colors['end'] + "\n>>>" + self.colors['end'])
        if inpt == 'y':
            client.drop_database(db)
            Menu.notification_queue.append("Database deleted.")
        else:
            Menu.notification_queue.append("Deletion canceled.")

    def sub_mark(self):
        # Mark/unmark a collection as temporary
        coll = self.get_coll_menu()
        if coll is None:
            return
        c_true = coll.find({"t_temp": True})
        c_false = coll.find({"t_temp": False})
        if c_true.count() > 0:  # we will assume we want to flip any t_temp = trues
            coll.update_many({"t_temp": True}, {'$set': {"t_temp": False}})
            Menu.notification_queue.append("Collection marked as permanent.")
        elif c_false.count() > 0:
            coll.update_many({"t_temp": False}, {'$set': {"t_temp": True}})
            Menu.notification_queue.append("Collection marked as temporary.")
        else:
            coll.insert_one({  # This creates a coll even if no tweets found.
                "t_temp": True
            })
            Menu.notification_queue.append("Collection marked as temporary.")
        c_true.close()
        c_false.close()

    def sub_strip_sentiment(self):
        # Remove sentiment values
        coll = self.get_coll_menu()
        if coll is None:
            return
        coll.update({},{"$unset":{"sentiment":1}},multi=True)
        Menu.notification_queue.append("Any sentiment values have been removed.")

    def sub_strip_read(self):
        # Remove reading values
        coll = self.get_coll_menu()
        if coll is None:
            return
        coll.update({},{"$unset":{"readability":1}},multi=True)
        Menu.notification_queue.append("Any readability values have been removed.")

    def sub_strip_facial(self):
        # Remove kairos values
        coll = self.get_coll_menu()
        if coll is None:
            return
        coll.update({},{"$unset":{"face":1}},multi=True)
        Menu.notification_queue.append("Any facial analysis values have been removed.")
