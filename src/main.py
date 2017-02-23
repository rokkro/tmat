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

def inputNum(msg, inpt_msg, lim, blank=False): #for typecasting to an int without a bazillion try..except's
    def reprint():
        print("\n" + msg)
    reprint()
    while True:
        inpt = input(inpt_msg)
        if inpt == 'p':
            reprint()
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
    i = inputNum("[1] - Scrape tweets.\n"
          "[2] - Perform Sentiment Analysis.\n"
          "[3] - Data Presentation.\n"
          "[4] - List Tweet Collections in DB.\n"
          "[5] - Purge temporary data\n","*Enter option number or 'p' to re-list options\n>>>",5)
    if i == 1:
        s = twitter.Setup()
        s.mongo_connect()
        search = s.search()
        limit = s.limit()
        while True:
            j = inputNum("[1] - Search = " + search + "\n[2] - Limit = " + str(limit) + "\n[3] - Temporary Collection = " + str(s.temp) +
                  "\n[4] - Image Filtering and Analysis = " + str(s.img) + "\n[5] - Database Name = '" + s.db_name +
                  "'\n[6] - Collection Name = '" + s.coll_name + "' (time will update when streaming starts)\n",
                                                                 "*Press 'Enter' to Begin, enter an option to change, "
                                                                 "or 'p' to re-list options\n>>>",6,True)
            if j == None:
                twitter.stream(search,limit,s.coll_name,s.db_name)
                break
            elif j == 1:
                search = s.search()
            elif j==2:
                limit = s.limit()
            elif j==3:
                if s.temp == False:
                    print(color.YELLOW,"**Collection marked as Temporary.**",color.END)
                    s.temp = True
                else:
                    print(color.YELLOW,"**Collection marked as Permanent.**",color.END)
                    s.temp = False
            elif j==4:
                s.img = True
            elif j==5:
                inpt = input("Enter a new name for the database, currently '" + s.db_name + "'. Leave blank to cancel.\n>>>")
                if inpt.strip() == '':
                    continue
                else:
                    print(color.YELLOW,"**Database changed from " + s.db_name + " to " + inpt + ".**",color.END)
                    s.db_name = inpt
        print(1)
    elif i == 2:
        print(2)
    elif i == 3:
        print(3)
    elif i == 4:
        print(4)
    elif i == 5:
        print(5)
    elif i == 6:
        print(6)
mode()
