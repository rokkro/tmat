import twitter

class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
# http://stackoverflow.com/a/17303428 for pretty font coloring

def color_msg(function): #simple message coloring
    print(color.YELLOW)
    function()
    print(color.END)

def get_input(msg,inpt_msg,lim,blank=False):
    while True:
        print("\n" + len(inpt_msg) * '-')
        print(msg)
        print(len(inpt_msg) * '-')
        i = input(color.BOLD + inpt_msg + color.END)
        if i == 'q':
            quit()
        elif i == '' and blank:
            break
        try:
            i = int(i)
        except ValueError:
            continue
        if i > lim or i < 1:
            continue
        else:
            return i
    return None

def mode():
    menu = {
        1: scrapeMode,
        2: exit,
        3: exit,
        4: exit,
        5: exit,
    }
    while True:
        i = get_input("[1] - Scrape tweets.\n"
              "[2] - Perform Sentiment Analysis.\n"
              "[3] - Data Presentation.\n"
              "[4] - List Databases and Collections.\n"
              "[5] - Purge temporary data","*Enter option number or [q] - quit.\n>>>",5)
        menu[i]()

def scrapeMode():
    s = twitter.Setup()
    color_msg(s.mongo_connect)
    search = s.search()
    limit = s.limit()
    while True:
        i = get_input("[1] - Search = '" + str(s.term).strip('\'[]\'') + "'\n[2] - Limit = " + str(s.lim) + "\n[3] - Temporary Collection = "+
            str(s.temp) + "\n[4] - Image Filtering and Analysis = " + str(s.img) + "\n[5] - Database Name = '" +
            s.db_name + "'\n[6] - Collection Name = '" + s.coll_name + "'\n[7] - MongoDB connected = " + color.YELLOW +
            str(s.connected) + color.END,"*Enter option number or: [Enter] - begin if MongoDB is connected, [q] - quit."
            "\n>>>", 7, True)
        if i == None and s.connected:
            twitter.stream(search, limit, s.coll_name, s.db_name)
            break

        def tmp_mod():
            @color_msg
            def tmp_chng():
                if s.temp == False:
                    print("**Collection will be marked as Temporary.**")
                    s.temp = True
                else:
                    print("**Collection will be marked as Permanent.**")
                    s.temp = False

        def img(): #IMAGE ANALYSIS
            if s.img:
                s.img = False
            else:
                s.img = True

        def db_mod():
            while True:
                inpt = input("Enter a new name for the database, currently '" + s.db_name + "'. Leave blank to cancel. "
                            "Spaces will be removed.\n>>>").replace(" ","")
                if inpt == '' or inpt == s.db_name:
                    break
                @color_msg
                def db_chng():
                    print("Database changed from '" + s.db_name + "' to '" + inpt + "'.")
                    s.db_name = inpt
                    if s.connected:
                        if inpt in s.dbname_list:
                            print("'" + inpt + "' already exists. New tweets will be added to existing.",end='')
                        else:
                            print("New database '" + inpt + "' will be created.",end='')
                break

        def coll_mod(): #COLLECTION NAME
            while True:
                inpt = input("Enter a new name for this collection, currently '" + s.coll_name +
                    "'. Leave blank to cancel.\nPut [dt] in name to insert date + time.\n>>>").strip()
                if inpt == '' or inpt == s.coll_name: #If blank or collection name is same
                    break
                coll_old = s.coll_name #temp variable for print statement below

                if '[dt]' in inpt: #inserting and replacing [dt] with date/time
                    s.coll_name = inpt.replace('[dt]',s.dt).strip()
                else:
                    s.coll_name = inpt
                @color_msg
                def coll_chng():
                    print( "Collection changed from '" + coll_old + "' to '" + s.coll_name + "'.")
                    if s.connected:
                        if s.coll_name in s.get_collections():
                            print("'" + s.coll_name + "' already exists. New tweets will be added to existing.",end='')
                        else:
                            print("New collection will be created.",end='')
                break

        def mongo():
            color_msg(s.mongo_connect) #cant pass params through dict, kinda a workaround

        menu = {
            1: s.search,
            2: s.limit,
            3: tmp_mod,
            4: img,
            5: db_mod,
            6: coll_mod,
            7: mongo
        }
        try:
            menu[i]()
        except TypeError: #ignores error from calling mongo var above.
            pass

if __name__ == "__main__":
    try:
        mode()
    except KeyboardInterrupt:
        pass
