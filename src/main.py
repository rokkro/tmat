import twitter
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
        search = s.search()
        limit = s.limit()
        j = inputNum("[1] - Search = " + search + "\n[2] - Limit = " + str(limit) + "\n[3] - Temporary Collection = " + str(s.temp) +
              "\n[4] - Image Filtering and Analysis = False\n[5] - Database Name = '" + s.db_name +
              "'\n[6] - Collection Name = '" + s.coll_name + "' (time will update when streaming starts)\n",
                                                             "*Press 'Enter' to Begin, enter an option to change, "
                                                             "or 'p' to re-list options\n>>>",6,True)
        if j == None:
            twitter.stream(search,limit,s.coll_name,s.db_name)
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
