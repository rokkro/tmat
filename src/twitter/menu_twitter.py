import mongo
from twitter.tweet_setup import Setup
from twitter.streaming import stream
from display import get_menu, Color


def menu_scrape():
    s = Setup()
    s.set_search()
    while True:
        inpt = get_menu(["Search = " + (str(s.term).strip('[]') if s.term else "None"),
                         "Limit = " + str(s.lim),
                         "Temporary Collection = " + str(s.temp),
                         "Database Name = '" + s.db_name + "'",
                         "Collection Name = '" + s.coll_name + "'",
                         "Tweet Similarity Threshold = " + str(s.sim),
                         "Languages = " + str(s.lang).strip('[]'),
                         "Follow UID(s) = " + (str(s.users).strip('[]') if s.users else "None"),
                         "MongoDB Connected = " + Color.YELLOW + str(mongo.connected) + Color.END],
                        "*Enter option number or: [Enter] - start streaming, [r] - return.""\n>>>", 9)

        if inpt == '' and mongo.connected and (s.term or s.users):
            print(Color.YELLOW)
            s.init_db()
            stream(s)
            print(Color.END)
            break
        elif inpt == '':
            print(Color.YELLOW + "MongoDB must be connected and a search or UID must have been entered." + Color.END)
            continue
        elif inpt == 'r':
            return

        def sub_search():
            print(Color.BOLD, end='')
            s.set_search()
            print(Color.END, end='')
            print(Color.YELLOW + "Search changed to " + (
                str(s.term).strip('[]') if s.term else "None") + "." + Color.END)

        def sub_lim():
            print(Color.BOLD, end='')
            s.set_limit()
            print(Color.END, end='')
            print(Color.YELLOW + "Limit changed to " + str(s.lim) + "." + Color.END)

        def sub_tmp():
            print(Color.YELLOW, end='')
            if not s.temp:
                print("Collection will be marked as Temporary.")
                s.temp = True
            else:
                print("Collection will be marked as Permanent.")
                s.temp = False
            print(Color.END, end='')

        def sub_db():
            while True:
                inpt = input(Color.BOLD + "Enter a new name for the database, currently '" + s.db_name +
                             "'. Leave blank to cancel.\nSpaces and special characters will be removed.\n>>>" + Color.END)
                inpt = ''.join(e for e in inpt if e.isalnum())
                if inpt == '' or inpt == s.db_name or inpt == 'admin' or inpt == 'local':
                    break
                print(Color.YELLOW + "Database changed from '" + s.db_name + "' to '" + inpt + "'.")
                s.db_name = inpt
                if mongo.connected:
                    if inpt in mongo.get_dbnames():
                        print("'" + inpt + "' already exists. New tweets will be added to existing.")
                    else:
                        print("New database '" + inpt + "' will be created.")
                print(Color.END, end='')
                break

        def sub_coll():
            while True:
                inpt = input(Color.BOLD + "Enter a new name for this collection, currently '" + s.coll_name +
                             "'. Leave blank to cancel.\nPut '[dt]' in name to insert date + time.\n>>>" +
                             Color.END).strip().replace("$", "")
                if inpt == '' or inpt == s.coll_name:  # If blank or collection name is same
                    break
                if '[dt]' in inpt:  # inserting and replacing [dt] with date/time
                    s.coll_name = inpt.replace('[dt]', s.dt).strip()
                else:
                    s.coll_name = inpt
                print(Color.YELLOW + "Collection changed to '" + s.coll_name + "'.")
                if mongo.connected:
                    if s.coll_name in mongo.get_collections(s.db_name):
                        print("'" + s.coll_name + "' already exists. New tweets will be added to existing.")
                    else:
                        print("New collection will be created.")
                print(Color.END, end='')
                break

        def sub_simil():
            while True:
                inpt = input(Color.BOLD + "*Enter a new value: 0.0 to 1.0. Higher value = filter out "
                                          "tweets with > similarity. Leave blank to cancel.\n>>>" + Color.END)
                if inpt == '' or inpt == s.sim:
                    break
                try:
                    inpt = float(inpt)
                    if inpt <= 1.0 and inpt >= 0:
                        s.sim = inpt
                    else:
                        raise ValueError
                    print(Color.YELLOW + "Similarity threshold set to " + str(s.sim) + "." + Color.END)
                    break
                except ValueError:
                    print("Invalid Input.")
                    continue

        def sub_lang():
            langs = ['en', 'ar', 'bn', 'cs', 'da', 'de', 'el', 'es', 'fa', 'fi', 'fil', 'fr', 'he', 'hi', 'hu', 'id',
                     'it',
                     'ja', 'ko', 'msa', 'nl', 'no', 'pl', 'pt', 'ro', 'ru', 'sv', 'th', 'tr', 'uk', 'ur', 'vl', 'zh-cn',
                     'zh-tw']
            inpt = input(Color.BOLD + "Enter a comma separated list of language codes. "
                                      "https://dev.twitter.com/web/overview/languages\n>>>").replace(" ", '').split(',')
            if inpt == '':
                return
            tmp = []
            for i in inpt:
                if i in langs and i not in tmp:
                    tmp.append(i)
            if len(tmp) >= 1:
                print(Color.YELLOW + "Accepted languages: " + str(tmp).strip("[]") + "." + Color.END)
                s.lang = tmp

        def sub_follow():
            print(Color.BOLD, end='')
            s.set_follow()
            print(Color.END, end='')
            print(Color.YELLOW + "Follow list changed to " + (
                str(s.users).strip('[]') if s.users else "None") + "." + Color.END)

        def sub_mongo():
            print(Color.YELLOW, end='')
            mongo.mongo_connection()
            print(Color.END, end='')

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
