import twitter, mongo

class color:
    YELLOW = '\033[93m'
    BOLD = '\033[1m'
    END = '\033[0m'

def get_input(msg, inpt_msg, lim):
    while True:
        print(len(inpt_msg) * '-')
        print(msg)
        print(len(inpt_msg) * '-')
        i = input(color.BOLD + inpt_msg + color.END)
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

def main_menu():
    print(color.YELLOW, end='')
    mongo.mongo_handler()
    print(color.END, end='')
    menu = {
        1: scrape_menu,
        2: exit,
        3: exit,
        4: exit,
        5: exit,
        6: exit,
    }
    while True:
        i = get_input("[1] - Scrape tweets.\n"
          "[2] - Perform Sentiment Analysis.\n"
          "[3] - Perform Image Analysis.\n"
          "[4] - Data Presentation.\n"
          "[5] - List Databases and Collections.\n"
          "[6] - Purge temporary data", "*Enter option number or [q] - quit.\n>>>", 5)
        try:
            menu[i]()
        except KeyError:
            pass

########################
def scrape_menu():  # menu for setting up tweet scraping
    s = twitter.Setup()
    search = s.search()
    limit = s.limit()
    while True:
        selection = get_input("[1] - Search = '" + str(s.term).strip('\'[]\'') + "'\n[2] - Limit = " + str(s.lim) +
            "\n[3] - Temporary Collection = " + str(s.temp) +
            "\n[4] - Database Name = '" + s.db_name + "'\n[5] - Collection Name = '" + s.coll_name +
            "'\n[6] - Tweet Similarity Threshold = " + str(s.similarity) +
            "\n[7] - Languages = " + str(s.language).strip('[]') +
            "\n[8] - MongoDB Connected = " + color.YELLOW + str(mongo.connected) + color.END,
            "*Enter option number or: [Enter] - begin if MongoDB is connected, [r] - return.""\n>>>",8)
        if selection == '' and mongo.connected:
            twitter.stream(search, limit, s.coll_name, s.db_name, s.temp, s.similarity,s.language)
            break

        elif selection == 'r':
            return

        elif selection == 1:
            s.search()
            print(color.YELLOW + "Search changed to '" + str(s.term).strip('\'[]\'') + "'." + color.END)

        elif selection == 2:
            s.limit()
            print(color.YELLOW + "Limit changed to " + str(s.lim) + "." + color.END)

        elif selection == 3:
            print(color.YELLOW, end='')
            if s.temp == False:
                print("Collection will be marked as Temporary.")
                s.temp = True
            else:
                print("Collection will be marked as Permanent.")
                s.temp = False
            print(color.END, end='')

        elif selection == 4:
            while True:
                inpt = input(color.BOLD + "Enter a new name for the database, currently '" + s.db_name +
                    "'. Leave blank to cancel. ""Spaces will be removed.\n>>>" + color.END).replace(" ", "")
                if inpt == '' or inpt == s.db_name:
                    break
                print(color.YELLOW + "Database changed from '" + s.db_name + "' to '" + inpt + "'.")
                s.db_name = inpt
                if mongo.connected:
                    if inpt in s.get_dbnames():
                        print("'" + inpt + "' already exists. New tweets will be added to existing.")
                    else:
                        print("New database '" + inpt + "' will be created.")
                print(color.END, end='')
                break

        elif selection == 5:
            while True:
                inpt = input(color.BOLD + "Enter a new name for this collection, currently '" + s.coll_name +
                    "'. Leave blank to cancel.\nPut '[dt]' in name to insert date + time.\n>>>" + color.END).strip()
                if inpt == '' or inpt == s.coll_name:  # If blank or collection name is same
                    break
                if '[dt]' in inpt:  # inserting and replacing [dt] with date/time
                    s.coll_name = inpt.replace('[dt]', s.dt).strip()
                else:
                    s.coll_name = inpt
                print(color.YELLOW + "Collection changed to '" + s.coll_name + "'.")
                if mongo.connected:
                    if s.coll_name in s.get_collections():
                        print("'" + s.coll_name + "' already exists. New tweets will be added to existing.")
                    else:
                        print("New collection will be created.")
                print(color.END, end='')
                break

        elif selection == 6:
            while True:
                inpt = input(color.BOLD + "Enter a new similarity threshold - 0.0 to 1.0. Higher value = filter out "
                    "higher similarity. Leave blank to cancel.\n>>>" + color.END)
                if inpt == '' or inpt == s.similarity:
                    break
                try:
                    inpt = float(inpt)
                    if inpt <= 1.0 and inpt >= 0:
                        s.similarity = inpt
                    else:
                        raise ValueError
                    print(color.YELLOW + "Similarity threshold set to " + str(s.similarity) + "." + color.END)
                    break
                except ValueError:
                    print("Invalid Input.")
                    continue

        elif selection == 7:
            langs = ['en','ar','bn','cs','da','de','el','es','fa','fi','fil','fr','he','hi','hu','id','it',
                     'ja','ko','msa','nl','no','pl','pt','ro','ru','sv','th','tr','uk','ur','vl','zh-cn','zh-tw']
            inpt = input(color.BOLD + "Enter a comma separated list of language codes. "
                "https://dev.twitter.com/web/overview/languages\n>>>").replace(" ",'').split(',')
            if inpt == '':
                break
            tmp = []
            for i in inpt:
                if i in langs and i not in tmp:
                    tmp.append(i)
            if len(tmp) >=1:
                print(color.YELLOW + "Accepted languages: " + str(tmp).strip("[]") + "." + color.END)
                s.language = tmp

        elif selection == 8:
            print(color.YELLOW, end='')
            mongo.mongo_handler()
            print(color.END, end='')
########################

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        pass
