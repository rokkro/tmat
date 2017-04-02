import mongo
from twitter.streaming import Setup, stream
from display import get_input, color
def menu_scrape():  # menu for setting up tweet scraping
    s = Setup()
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
            stream(s.term, s.lim, s.coll_name, s.db_name, s.temp, s.sim, s.lang, s.users)
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
            mongo.mongo_connection()
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
