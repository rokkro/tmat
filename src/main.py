import twitter

class color:
    YELLOW = '\033[93m'
    BOLD = '\033[1m'
    END = '\033[0m'

def get_input(msg,inpt_msg,lim,blank=False):
    while True:
        print("\n" + len(inpt_msg) * '-')
        print(msg)
        print(len(inpt_msg) * '-')
        i = input(color.BOLD + inpt_msg + color.END)
        if i == 'q':
            quit()
        elif i == 'r' and blank: 
            return 'r'
        elif i == '' and blank:
            return None
        try:
            i = int(i)
        except ValueError:
            continue
        if i > lim or i < 1:
            continue
        else:
            return i

def main_menu():
    menu = {
        1: scrape_menu,
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

########################
def scrape_menu(): #menu for setting up tweet scraping
    s = twitter.Setup()
    print(color.YELLOW,end='')
    s.mongo_handler()
    print(color.END,end='')
    search = s.search()
    limit = s.limit()
    while True:
        selection = get_input("[1] - Search = '" + str(s.term).strip('\'[]\'') + "'\n[2] - Limit = " + str(s.lim) +
            "\n[3] - Temporary Collection = "+str(s.temp) + "\n[4] - Image Filtering and Analysis = " + str(s.img) +
            "\n[5] - Database Name = '" +s.db_name + "'\n[6] - Collection Name = '" + s.coll_name +
            "'\n[7] - MongoDB connected = " + color.YELLOW +str(s.connected) + color.END,
            "*Enter option number or: [Enter] - begin if MongoDB is connected, [r] - return.""\n>>>", 7, True)
        if selection == None and s.connected:
            twitter.stream(search, limit, s.coll_name, s.db_name)
            break

        elif selection == 'r':
            return

        elif selection == 1:
            s.search()

        elif selection == 2:
            s.limit()

        elif selection == 3:
            print(color.YELLOW,end='')
            if s.temp == False:
                print("**Collection will be marked as Temporary.**")
                s.temp = True
            else:
                print("**Collection will be marked as Permanent.**")
                s.temp = False
            print(color.END,end='')

        elif selection == 4:
            if s.img:
                s.img = False
            else:
                s.img = True

        elif selection == 5:
            while True:
                inpt = input("Enter a new name for the database, currently '" + s.db_name +
                    "'. Leave blank to cancel. ""Spaces will be removed.\n>>>").replace(" ","")
                if inpt == '' or inpt == s.db_name:
                    break
                print(color.YELLOW,"Database changed from '" + s.db_name + "' to '" + inpt + "'.")
                s.db_name = inpt
                if s.connected:
                    if inpt in s.dbname_list:
                        print("'" + inpt + "' already exists. New tweets will be added to existing.",end='')
                    else:
                        print("New database '" + inpt + "' will be created.",end='')
                print(color.END,end='')
                break

        elif selection == 6:
            while True:
                inpt = input("Enter a new name for this collection, currently '" + s.coll_name +
                    "'. Leave blank to cancel.\nPut [dt] in name to insert date + time.\n>>>").strip()
                if inpt == '' or inpt == s.coll_name: #If blank or collection name is same
                    break
                if '[dt]' in inpt: #inserting and replacing [dt] with date/time
                    s.coll_name = inpt.replace('[dt]',s.dt).strip()
                else:
                    s.coll_name = inpt
                print(color.YELLOW,"Collection changed to '" + s.coll_name + "'.")
                if s.connected:
                    if s.coll_name in s.get_collections():
                        print("'" + s.coll_name + "' already exists. New tweets will be added to existing.",end='')
                    else:
                        print("New collection will be created.",end='')
                print(color.END,end='')
                break

        elif selection == 7:
            print(color.YELLOW,end='')
            s.mongo_handler()
            print(color.END,end='')
########################

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        pass
