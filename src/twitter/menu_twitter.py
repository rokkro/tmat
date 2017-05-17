import mongo
from twitter.tweet_setup import Setup
from twitter.streaming import stream
from twitter.historical import scrape
from display import get_menu, Color


def sub_search(s):
    print(Color.BOLD, end='')
    if s.streaming:
        print(Color.BOLD + "*Enter search term(s), separate multiple queries with '||'.")
    else:
        print(Color.BOLD + "*Enter search term(s), use https://dev.twitter.com/rest/public/search for operators.")
    inpt = input("*Leave blank to clear, [r] - return.\n>>>" + Color.END).strip()
    print(Color.END,end='')
    if inpt == 'r':
        return
    s.set_search(inpt)
    print(Color.END, end='')
    print(Color.YELLOW + "Search changed to " + (
        str(s.term).strip('[]') if s.term else "None") + "." + Color.END)


def sub_lim(s):
    print(Color.BOLD, end='')
    inpt = get_menu('',None, "*Enter number of tweets to retrieve. Leave blank for unlimited.\n>>>")
    if inpt == 'r':
        return
    if inpt == '':
        s.lim = None
    else:
        s.lim = inpt
    print(Color.END, end='')
    print(Color.YELLOW + "Limit changed to " + str(s.lim) + "." + Color.END)


def sub_tmp(s):
    print(Color.YELLOW, end='')
    if not s.temp:
        print("Collection will be marked as Temporary.")
        s.temp = True
    else:
        print("Collection will be marked as Permanent.")
        s.temp = False
    print(Color.END, end='')


def sub_db(s):
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


def sub_coll(s):
    while True:
        inpt = input(Color.BOLD + "Enter a new name for this collection, currently '" + s.coll_name +
                     "'. Leave blank to cancel.\nPut '[dt]' in name to insert date + time.\n>>>" +
                     Color.END).strip().replace("$", "")
        if inpt == '' or inpt == s.coll_name:  # If blank or collection name is same
            break
        if '[dt]' in inpt:  # inserting and replacing [dt] with date/time
            s.coll_name = inpt.replace('[dt]', str(s.get_dt())).strip()
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


def sub_simil(s):
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


def sub_lang(s):
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


def sub_follow(s):
    print(Color.BOLD, end='')
    print("Use http://gettwitterid.com to get a UID from a username. Must be a numeric value.")
    inpt = input(Color.BOLD + "*Enter UID(s), separate with '||'. Leave blank for no user tracking, [r] - "
                           "return/cancel.\n>>>" + Color.END).strip()
    if inpt == 'r':
        return
    s.set_follow(inpt)
    print(Color.END, end='')
    print(Color.YELLOW + "Follow list changed to " + (
        str(s.users).strip('[]') if s.users else "None") + "." + Color.END)


def sub_mongo(s):
    print(Color.YELLOW, end='')
    mongo.mongo_connection()
    print(Color.END, end='')

def menu_stream():
    s = Setup(True)
    sub_search(s)
    print("\n")
    while True:
        inpt = get_menu("STREAMING",["Search = " + (str(s.term).strip('[]') if s.term else "None"),
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
        menu[inpt](s)
def sub_result(s):
    inpt = input(Color.BOLD + "*Enter a result type: 'mixed','recent', or 'popular'.\n>>>" + Color.END).strip()
    s.set_result_type(inpt)
    print(Color.YELLOW + "Result type set to " + s.result_type + "." + Color.END)

def sub_date(s):
    inpt = input(
        Color.BOLD + "*Enter a tweet cut off date. Must be in the format YYYY-MM-DD and no older than 7 days.\n"
                     "*Leave blank to clear, [r] - cancel.\n>>>" + Color.END)
    inpt = inpt.strip().replace(" ", "")
    if inpt == "":
        s.until = None
        return
    elif inpt == "r":
        return
    print(Color.YELLOW,end="")
    s.set_date(inpt)
    print(Color.END,end="")

def menu_hist():
    s = Setup()
    sub_search(s)
    sub_lim(s)
    print("\n")
    while True:
        inpt = get_menu("HISTORIC",["Search = " + (str(s.term).strip('[]') if s.term else "None"),
                         "Limit = " + str(s.lim),
                         "Temporary Collection = " + str(s.temp),
                         "Database Name = '" + s.db_name + "'",
                         "Collection Name = '" + s.coll_name + "'",
                         "Tweet Similarity Threshold = " + str(s.sim),
                         "Result Type = " + s.result_type,
                         "Before Date = " + str(s.until),
                         "MongoDB Connected = " + Color.YELLOW + str(mongo.connected) + Color.END],
                        "*Enter option number or: [Enter] - start streaming, [r] - return.""\n>>>", 9)

        if inpt == '' and mongo.connected and s.term and s.lim:
            print(Color.YELLOW)
            s.init_db()
            scrape(s)
            print(Color.END)
            break
        elif inpt == '':
            print(Color.YELLOW + "MongoDB must be connected, and both a search and limit must have been entered." + Color.END)
            continue

        menu = {
            1: sub_search,
            2: sub_lim,
            3: sub_tmp,
            4: sub_db,
            5: sub_coll,
            6: sub_simil,
            7: sub_result,
            8: sub_date,
            9: sub_mongo
        }
        menu[inpt](s)
