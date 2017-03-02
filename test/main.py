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
def mongo(s):
    print(color.YELLOW)
    s.mongo_connect() #CONNECTS TO MONGODB
    print(color.END)


class msg():
    def __init__(self,msg,inptmsg,lim,blank=False):
        self.msg = msg
        self.inptmsg = inptmsg
        self.lim = lim
        self.blank = blank

    def get_input(self):
        while True:
            i =  input(self.inptmsg)
            if i == 'p':
                self.print_opt()
            elif i == 'q':
                quit()
            elif i == '' and self.blank:
                break
            try:
                i = int(i)
            except ValueError:
                continue
            if i > self.lim or i < 1:
                continue
            else:
                return i
        return None

    def print_opt(self):
        print(self.msg)


def inputNum(msg, inpt_msg, lim, blank=False): #for typecasting to an int without a bazillion try..except's
    def reprint():
        print("\n" + msg)
    reprint()
    while True:
        inpt = input(inpt_msg)
        if inpt == 'p':
            reprint()
        elif inpt == 'q':
            quit()
        if inpt == '' and blank:
            break
        try:
            inpt = int(inpt)
        except ValueError:
            continue
        if inpt > lim or inpt < 1:
            continue
        else:
            return inpt
    return None

def mode():
    s = twitter.Setup()
    while True:
        i = inputNum("[1] - Scrape tweets.\n"
              "[2] - Perform Sentiment Analysis.\n"
              "[3] - Data Presentation.\n"
              "[4] - List Databases and Collections.\n"
              "[5] - Purge temporary data\n","*Enter option number or: 'p' - re-print, 'q' - quit.\n>>>",5)
        if i == 1:
            scrapeMode(s)
        elif i == 2:
            print(2)
        elif i == 3:
            print(3)
        elif i == 4:
            '''
            mongo(s)
            if s.connected:
                while True:
                    print("DATABASES:")
                    for j in range(0,len(s.dbname_list)):
                        print('[' + str(j) + '] - ' + s.dbname_list[j] )
                    inp = int(input("Enter DB number:"))
                    s.db_name = s.dbname_list[inp]
                    print("COLLECTIONS")
                    for j in range(0,len(s.get_collections())):
                        print('[' + str(j) + '] - ' + s.get_collections()[j])
             '''
        elif i == 5:
            print(5)
        elif i == 6:
            print(6)

def scrapeMode(s):
    mongo(s)
    search = s.search()
    limit = s.limit()
    while True:
        i = inputNum("[1] - Search = '" + str(search).strip('\'[]\'') + "'\n[2] - Limit = " + str(limit) + "\n[3] - Temporary Collection = "+
            str(s.temp) + "\n[4] - Image Filtering and Analysis = " + str(s.img) + "\n[5] - Database Name = '" +
            s.db_name + "'\n[6] - Collection Name = '" + s.coll_name + "'\n[7] - MongoDB connected = " + color.YELLOW +
            str(s.connected) + color.END,"*Enter an option to change or press 'Enter' to begin if MongoDB is connected."
            "\n>>>", 7, True)
        if i == None and s.connected:
            twitter.stream(search, limit, s.coll_name, s.db_name)
            break
        elif i == 1: #SEARCH
            search = s.search()
        elif i == 2: #SET LIMIT
            limit = s.limit()
        elif i == 3: #TEMP OR PERMANENT
            if s.temp == False:
                print(color.YELLOW, "**Collection marked as Temporary.**", color.END)
                s.temp = True
            else:
                print(color.YELLOW, "**Collection marked as Permanent.**", color.END)
                s.temp = False
        elif i == 4: #IMAGE ANALYSIS
            s.img = True

        elif i == 5: #DATABASE NAME
            inpt = input("Enter a new name for the database, currently '" + s.db_name + "'. Leave blank to cancel. "
                        "Spaces will be removed.\n>>>").replace(" ","")
            if inpt == '' or inpt == s.db_name:
                continue
            print(color.YELLOW, "**Database changed from '" + s.db_name + "' to '" + inpt + "'.", end='')
            s.db_name = inpt

            if s.connected:
                if inpt in s.dbname_list:
                    print("'" + inpt + "' already exists. New tweets will be added to existing.**", color.END)
                else:
                    print("New database '" + inpt + "' will be created.**", color.END)
            else:
                print("**", color.END)

        elif i == 6: #COLLECTION NAME
            inpt = input("Enter a new name for this collection, currently '" + s.coll_name +
                "'. Leave blank to cancel.\nPut [+dt] in name to insert date + time.\n>>>").strip()
            if inpt == '' or inpt == s.coll_name: #If blank or collection name is same
                continue
            coll_old = s.coll_name #temp variable for print statement below

            if '[+dt]' in inpt: #inserting and replacing [+dt] with date/time
                s.coll_name = inpt.replace('[+dt]',s.dt).strip()
            else:
                s.coll_name = inpt
            print(color.YELLOW, "**Collection changed from '" + coll_old + "' to '" + s.coll_name + "'.", end=' ')

            if s.connected:
                if s.coll_name in s.get_collections():
                    print("'" + s.coll_name + "' already exists. Tweets will be added to existing.**",color.END)
                else:
                    print("New collection '" + s.coll_name + "' will be created.**",color.END)
            else:
                print("**",color.END)

        elif i == 7: #CONNECTION TO MONGODB
            mongo(s)

if __name__ == "__main__":
    try:
        mode()
    except KeyboardInterrupt:
        pass
